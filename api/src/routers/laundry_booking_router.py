"""Routes for laundry booking."""
import datetime as dt

import fastapi as fa
from fastapi import security as fas

import mongodb
from auth.models import user
from laundry_booking import laundry_booking as lb
from laundry_booking import lb_types as lbt
from routers.auth_router import authenticator

router = fa.APIRouter()


@router.get("/getweek")
async def get_week(
    user_me: user.UserBase = fa.Depends(authenticator.get_current_user),
    offset: int = 0,
) -> lbt.WeekSlotsDict:
    """Get the slots data for the requested week."""
    # TODO: Get currently booked slots from the DB and pass to the
    # Laundry Booking Manager during instantiation for correct parsing
    # of the current slots statuses.
    now = dt.datetime.now()
    lbm = lb.LaundryBookingManager(offset=offset, target_datetime=now)
    return lbm.week_slots
