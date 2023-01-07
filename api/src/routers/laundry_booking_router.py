"""Routes for laundry booking."""
import datetime as dt

import fastapi as fa
from fastapi import security as fas

import mongodb
from auth.models import user as auth_user
from laundry_booking import laundry_booking as lb
from laundry_booking import lb_types as lbt
from laundry_booking.models import user as lb_user
from routers.auth_router import authenticator

lb_user_coll = mongodb.mongo_db_conn.get_coll(
    db_name="dc_laundry_booking", coll_name="users"
)

router = fa.APIRouter()


@router.post("/add_user")
async def add_user(
    user_add: lb_user.UserAdd,
    user_me: auth_user.UserBase = fa.Depends(authenticator.get_current_user),
):
    """Add a user to the Laundry Booking DB.

    The user must already exist in the Auth DB, and now they complete their data for the
    Laundry Booking DB.
    """
    user_add.upsert(user_coll=lb_user_coll, username=user_me.username)
    return user_add


@router.get("/getweek")
async def get_week(
    user_me: auth_user.UserBase = fa.Depends(authenticator.get_current_user),
    offset: int = 0,
) -> lbt.WeekSlotsDict:
    """Get the slots data for the requested week."""
    # TODO: Get currently booked slots from the DB and pass to the
    # Laundry Booking Manager during instantiation for correct parsing
    # of the current slots statuses.
    now = dt.datetime.now()
    lbm = lb.LaundryBookingManager(offset=offset, target_datetime=now)
    return lbm.week_slots
