"""Routes for laundry booking."""
import datetime as dt
import typing as t

import fastapi as fa
import pydantic as pyd

from src import auth
from src import laundry_booking as lb
from src import mongodb
from src.laundry_booking import models as lb_m
from src.laundry_booking.utils import date_parsing as lb_dp
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


@router.get("/getweek")
async def get_week(
    token: str = fa.Depends(auth_router.oauth2_scheme),
    offset: int = 0,
) -> lb_m.WeekSlotsDict:
    """Get the slots data for the requested week."""
    token_data = auth.decode_token(token)

    db_user = lb_user.User.get(
        user_coll=lb_user_coll,
        username=token_data.username,
    )

    bookings_by_user = db_user.get_bookings()

    bookings_by_others = db_user.get_bookings_by_others(
        user_coll=lb_user_coll,
        username=token_data.username,
    )

    now = dt.datetime.now()

    lb_manager = lb.LaundryBookingManager(
        offset=offset,
        target_datetime=now,
        slots_booked_by_others=bookings_by_others,
        slots_booked_by_user=bookings_by_user,
    )
    return lb_manager.week_slots


class BookSlotReqBody(pyd.BaseModel):
    """Model for the body of a book_slot request."""

    date_str: str
    slot_id: lb_m.SlotIdInt


@router.post("/book_slot")
async def book_slot(
    req_body: BookSlotReqBody,
    token: str = fa.Depends(auth_router.oauth2_scheme),
):
    """Book a slot given a date and slot_id."""
    # Check that the date format is correct.
    try:
        date = lb_dp.parse_date_from_string(req_body.date_str)
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

    # If the user already has a booking for the given date, then they cannot add another
    # booking for that very same date.
    bookings_by_user = user_db.get_bookings()
    if date in bookings_by_user:
        if req_body.slot_id in bookings_by_user[date]:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_409_CONFLICT,
                detail="User has already booked the selected slot.",
            )
        else:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_409_CONFLICT,
                detail="User already has a booked slot for the selected date.",
            )

    # If the slot_id is already taken by someone else, it cannot be booked.
    bookings_by_others = user_db.get_bookings_by_others(
        user_coll=lb_user_coll, username=token_data.username
    )
    if date in bookings_by_others and req_body.slot_id in bookings_by_others[date]:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail="The selected slot is already booked by someone else.",
        )

    # If here, the slot is actually available for the user, so we try to book it.
    result = user_db.add_booking(
        user_coll=lb_user_coll,
        username=token_data.username,
        date_str=req_body.date_str,
        slot_id=req_body.slot_id,
    )

    return {
        "username": token_data.username,
        "full name": user_db.name,
        "date": date,
        "slot_id": int(req_body.slot_id),
        "matched_count": str(result.matched_count),
    }
