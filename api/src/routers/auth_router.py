"""Routes for authentication."""
import fastapi as fa
import pymongo.results as pym_res
from fastapi import security as fas

from src import auth, mongodb
from src.mongodb.models.auth import user as auth_user

user_coll = mongodb.mongo_db_conn.get_coll(db_name="dc_slot_booking", coll_name="auth")

router = fa.APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = fas.OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register")
async def register(new_user: auth_user.UserRegister):
    """Registers a new user."""
    # Parse new user to validate username and password and get the hashed password.
    parsed_new_user = auth.parse_new_user(
        username=new_user.username, password=new_user.password
    )

    new_user_db = auth_user.UserDB(
        username=new_user.username,
        email=new_user.email,
        disabled=False,
        hashed_password=parsed_new_user.hashed_password,
    )

    insert_one_result: pym_res.InsertOneResult = new_user_db.add(user_coll=user_coll)
    new_user_id = str(insert_one_result.inserted_id)

    return {"id_": new_user_id}


@router.post("/login")
async def login(form_data: fas.OAuth2PasswordRequestForm = fa.Depends()):
    """Logins a user (using username and password) and returns a token."""
    user_from_db = auth_user.UserDB.get(
        user_coll=user_coll, username=form_data.username
    )

    try:
        token = auth.authenticate_user(
            username=form_data.username,
            password=form_data.password,
            hashed_password=user_from_db.hashed_password,
        )
    except ValueError as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return token


@router.get("/users/me")
async def get_users_me(token: str = fa.Depends(oauth2_scheme)):
    """Get the user making the request taken from the bearer token."""
    token_data = auth.decode_token(token)
    user_db = auth_user.UserDB.get(user_coll=user_coll, username=token_data.username)
    if user_db.disabled:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    # Filter out sensitive data and return.
    user = auth_user.UserBase(**user_db.dict())
    return user
