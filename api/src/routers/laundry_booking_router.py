"""Routes for laundry booking."""
import datetime as dt

import fastapi as fa
from src.auth import models as auth_models
from src.laundry_booking import models as lb_models
from src.mongodb.models.laundry_booking import user as lb_user

from src import auth
from src import laundry_booking as lb
from src import mongodb

lb_user_coll = mongodb.mongo_db_conn.get_coll(
    db_name="dc_laundry_booking", coll_name="users"
)

router = fa.APIRouter(
    prefix="/booking",
    tags=["booking"],
)


@router.post("/add_user")
async def add_user(
    user_add: lb_user.UserAdd,
    token_data: auth_models.TokenData = fa.Depends(auth.decode_token),
) -> lb_user.UserAdd:
    """Add a user to the Laundry Booking DB.

    The user must already exist in the Auth DB, and now they complete their data for the
    Laundry Booking DB.
    """
    user_add.upsert(user_coll=lb_user_coll, username=token_data.username)
    return user_add


@router.get("/getweek")
async def get_week(
    token_data: auth_models.TokenData = fa.Depends(auth.decode_token),
    offset: int = 0,
) -> lb_models.WeekSlotsDict:
    """Get the slots data for the requested week."""
    # TODO: Get currently booked slots from the DB and pass to the
    # Laundry Booking Manager during instantiation for correct parsing
    # of the current slots statuses.
    now = dt.datetime.now()
    lb_manager = lb.LaundryBookingManager(offset=offset, target_datetime=now)
    return lb_manager.week_slots
