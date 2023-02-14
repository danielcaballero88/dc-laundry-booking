"""Script to write some users to the DB for testing and development.

Run with:
$ docker compose run -rm dc-slot-booking_api python -m src.data.init_db
"""
import json
import os
import typing as t

from src import auth as a
from src import mongodb as m
from src.mongodb.models.auth import user as au
from src.mongodb.models.slot_booking import user as sbu

HERE = os.path.dirname(__file__)

AUTH_USER_COLL = m.mongo_db_conn.get_coll(db_name="dc_slot_booking", coll_name="auth")
SB_USER_COLL = m.mongo_db_conn.get_coll(db_name="dc_slot_booking", coll_name="users")


class TestUserDict(t.TypedDict):
    username: str
    email: str
    password: str
    appartment: int
    name: str
    bookings: dict[str, int]


def get_test_users() -> list[TestUserDict]:
    """Read and parse test users data form the json file."""
    with open(
        file=os.path.join(HERE, "users.json"),
        mode="r",
        encoding="utf-8",
    ) as json_file:
        test_users_data = json.load(json_file)

    users: list[TestUserDict] = test_users_data["custom_users"]
    num_test_users: int = test_users_data["num_test_users"]

    for num in range(num_test_users):
        test_user: TestUserDict = {
            "username": f"test_user_{num}",
            "email": f"test_user_{num}@test_user_{num}.test_user_{num}",
            "password": f"test_user_{num}",
            "appartment": 0,
            "name": f"Test User {num}",
            "bookings": {},
        }
        users.append(test_user)

    return users


def write_user_to_db(test_user: TestUserDict) -> None:
    """Write a test user to the DB.

    The user data goes into two collections:
    - auth: for auth related data.
    - users: for slot bookings data.
    """
    new_user = au.UserRegister(
        username=test_user["username"],
        email=test_user["email"],
        password=test_user["password"],
    )
    parsed_new_user = a.parse_new_user(
        username=test_user["username"],
        password=test_user["password"],
    )
    new_user_db = au.UserDB(
        username=new_user.username,
        email=new_user.email,
        disabled=False,
        hashed_password=parsed_new_user.hashed_password,
    )
    new_user_db.add(user_coll=AUTH_USER_COLL)

    sb_user = sbu.UserAdd(
        appartment=test_user["appartment"],
        name=test_user["name"],
        bookings=test_user["bookings"],
    )
    sb_user.upsert(user_coll=SB_USER_COLL, username=test_user["username"])


def write_users_to_db(test_users: list[TestUserDict]) -> None:
    """Write a list of test users to the DB."""
    for test_user in test_users:
        write_user_to_db(test_user)


def main():
    """Main script function."""
    test_users = get_test_users()
    write_users_to_db(test_users)


if __name__ == "__main__":
    main()
