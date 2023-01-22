"""Routes for laundry booking."""
import datetime as dt
import typing as t

import fastapi as fa
import pydantic as pyd

from src import auth
from src import laundry_booking as lb
from src import mongodb
from src.laundry_booking import models as lb_m
from src.laundry_booking.utils import datetime_utils as lb_dt_u
from src.mongodb.models.laundry_booking import user as lb_user
from src.routers import auth_router

lb_user_coll = mongodb.mongo_db_conn.get_coll(
    db_name="dc_laundry_booking", coll_name="users"
)

router = fa.APIRouter(
    prefix="/booking",
    tags=["booking"],
)


def _parse_slot_id_from_string(slot_id: lb_m.SlotIdStr) -> lb_m.SlotIdInt:
    return t.cast(lb_m.SlotIdInt, int(slot_id))


@router.post("/add_user")
async def add_user(
    user_add: lb_user.UserAdd,
    token: str = fa.Depends(auth_router.oauth2_scheme),
) -> lb_user.UserAdd:
    """Add a user to the Laundry Booking DB.

    The user must already exist in the Auth DB, and now they complete their data for the
    Laundry Booking DB.
    """
    token_data = auth.decode_token(token)
    user_add.upsert(user_coll=lb_user_coll, username=token_data.username)
    return user_add


def _init_lb_manager(
    username: str,
    user_db: lb_user.User,
    target_datetime: dt.datetime,
    offset: int,
) -> lb.LaundryBookingManager:
    bookings_by_user = user_db.get_bookings()

    bookings_by_others = user_db.get_bookings_by_others(
        user_coll=lb_user_coll,
        username=username,
    )

    lb_manager = lb.LaundryBookingManager(
        offset=offset,
        target_datetime=target_datetime,
        slots_booked_by_others=bookings_by_others,
        slots_booked_by_user=bookings_by_user,
    )

    return lb_manager


@router.get("/get_week")
async def get_week(
    token: str = fa.Depends(auth_router.oauth2_scheme),
    offset: int = 0,
) -> lb_m.WeekSlotsDict:
    """Get the slots data for the requested week."""
    token_data = auth.decode_token(token)

    now = dt.datetime.now()

    user_db = lb_user.User.get(
        user_coll=lb_user_coll,
        username=token_data.username,
    )

    lb_manager = _init_lb_manager(
        username=token_data.username,
        user_db=user_db,
        target_datetime=now,
        offset=offset,
    )

    return lb_manager.week_slots


class BookSlotReqBody(pyd.BaseModel):
    """Model for the body of a book_slot request."""

    date_str: str
    slot_id: lb_m.SlotIdInt


class BookSlotResp(pyd.BaseModel):
    """Model for the response of the book_slot method."""

    username: str
    full_name: str
    date: str
    slot_id: lb_m.SlotIdInt
    matched_count: str


def _get_week_for_booking_slot(
    username: str,
    date: dt.date,
    user_db: lb_user.User,
) -> lb.LaundryBookingManager:
    """Before booking/unbooking a slot, get the week slots."""
    # Calculate the offset needed to get the correct week.
    now = dt.datetime.now()
    today = now.date()
    offset = ((date - today).days - (7 - today.weekday())) // 7 + 1

    lb_manager = _init_lb_manager(
        username=username,
        user_db=user_db,
        target_datetime=now,
        offset=offset,
    )

    return lb_manager


@router.post("/book_slot")
async def book_slot(
    req_body: BookSlotReqBody,
    token: str = fa.Depends(auth_router.oauth2_scheme),
) -> BookSlotResp:
    """Book a slot given a date and slot_id."""
    # Check that the date format is correct.
    try:
        date = lb_dt_u.parse_date_from_string(req_body.date_str)
    except Exception as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Bad date format, please use YYYY-MM-DD.",
        ) from exc

    # Get user data from the DB.
    token_data = auth.decode_token(token)
    user_db = lb_user.User.get(
        user_coll=lb_user_coll,
        username=token_data.username,
    )

    lb_manager = _get_week_for_booking_slot(
        username=token_data.username,
        date=date,
        user_db=user_db,
    )

    date = lb_dt_u.parse_date_from_string(req_body.date_str)
    date_slots = lb_manager.week_slots[date]
    slot_id = req_body.slot_id
    target_slot_status = date_slots[slot_id]

    if target_slot_status == lb_m.SlotsStatus.UNAVAILABLE.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="Selected slot is unavailable.",
        )
    if target_slot_status == lb_m.SlotsStatus.BOOKED_BY_USER.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="Selected slot is already booked by user.",
        )
    if target_slot_status == lb_m.SlotsStatus.BOOKED_BY_OTHER.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="Selected slot is already booked by another user.",
        )
    if lb_m.SlotsStatus.BOOKED_BY_USER.value in date_slots.values():
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="The user already has a booking for the same date.",
        )
    if target_slot_status != lb_m.SlotsStatus.AVAILABLE.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="Unexpected error.",
        )

    # If here, the slot is actually available for the user, so we try to book it.
    result = user_db.add_booking(
        user_coll=lb_user_coll,
        username=token_data.username,
        date_str=req_body.date_str,
        slot_id=req_body.slot_id,
    )

    return BookSlotResp(
        username=token_data.username,
        full_name=user_db.name,
        date=req_body.date_str,
        slot_id=req_body.slot_id,
        matched_count=str(result.matched_count),
    )


@router.delete("/unbook_slot")
async def unbook_slot(
    req_body: BookSlotReqBody,
    token: str = fa.Depends(auth_router.oauth2_scheme),
):
    """Delete a booked slot."""
    # TODO: Avoid the repeated code between this function and book_slot.

    # Check that the date format is correct.
    try:
        date = lb_dt_u.parse_date_from_string(req_body.date_str)
    except Exception as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Bad date format, please use YYYY-MM-DD.",
        ) from exc

    # Get user data from the DB.
    token_data = auth.decode_token(token)
    user_db = lb_user.User.get(
        user_coll=lb_user_coll,
        username=token_data.username,
    )

    lb_manager = _get_week_for_booking_slot(
        username=token_data.username,
        date=date,
        user_db=user_db,
    )

    date = lb_dt_u.parse_date_from_string(req_body.date_str)
    date_slots = lb_manager.week_slots[date]
    slot_id = req_body.slot_id
    target_slot_status = date_slots[slot_id]

    if target_slot_status != lb_m.SlotsStatus.BOOKED_BY_USER.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="Cannot unbook this slot because it's not booked by the user.",
        )

    result = user_db.delete_booking(
        user_coll=lb_user_coll,
        username=token_data.username,
        date_str=req_body.date_str,
        slot_id=req_body.slot_id,
    )

    return BookSlotResp(
        username=token_data.username,
        full_name=user_db.name,
        date=req_body.date_str,
        slot_id=req_body.slot_id,
        matched_count=str(result.matched_count),
    )
