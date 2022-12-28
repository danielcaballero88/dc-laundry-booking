"""Main module for the API."""
import auth
import fastapi as fa
import mongodb
from auth.models import user
from fastapi import security as fas

app = fa.FastAPI()


@app.on_event("startup")
async def startup():
    """Open MongoDB Client on app startup."""
    mongodb.mongo_db_conn.open_client()


@app.on_event("shutdown")
async def shutdown():
    """Open MongoDB Client on app shutdown."""
    mongodb.mongo_db_conn.close_client()


user_coll = mongodb.mongo_db_conn.get_coll(
    db_name="dc_laundry_booking", coll_name="auth"
)

authenticator = auth.Authenticator(user_coll=user_coll)


@app.get("/")
async def hello_world():
    """Returns Hello World."""
    return {"Hello": "World"}


@app.post("/register")
async def register(new_user: user.UserRegister):
    """Registers a new user."""
    new_user_id = authenticator.register_new_user(new_user)
    return {"id_": new_user_id}


@app.post("/login")
async def login(form_data: fas.OAuth2PasswordRequestForm = fa.Depends()):
    """Logins a user (using username and password) and returns a token."""
    token = authenticator.authenticate_user(form_data.username, form_data.password)
    return token


@app.get("/users/me")
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
