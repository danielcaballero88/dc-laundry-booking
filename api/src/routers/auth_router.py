"""Routes for authentication."""
import fastapi as fa
from fastapi import security as fas

import auth
import mongodb
from auth.models import user

user_coll = mongodb.mongo_db_conn.get_coll(
    db_name="dc_laundry_booking", coll_name="auth"
)

authenticator = auth.Authenticator(user_coll=user_coll)


router = fa.APIRouter()


@router.post("/register")
async def register(new_user: user.UserRegister):
    """Registers a new user."""
    new_user_id = authenticator.register_new_user(new_user)
    return {"id_": new_user_id}


@router.post("/login")
async def login(form_data: fas.OAuth2PasswordRequestForm = fa.Depends()):
    """Logins a user (using username and password) and returns a token."""
    token = authenticator.authenticate_user(form_data.username, form_data.password)
    return token


@router.get("/users/me")
async def get_users_me(
    user_me: user.UserBase = fa.Depends(authenticator.get_current_user),
):
    """Get the user making the request.

    GET /users/me gets the data of the user associated with the bearer
    token passed for authentication in the headers.

    Dependency injection:
    - user.get_current_active_user(UserBase) -> UserBase
        - user.get_current_user(token) -> UserBase
    """
    return user_me
