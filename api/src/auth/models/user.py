"""Module to interact with the "user" collection."""

from __future__ import annotations

from typing import Optional

import fastapi as fa
import pydantic as pyd
import pymongo.collection as pym_coll
import pymongo.errors as pym_err
import pymongo.results as pym_res


class UserBase(pyd.BaseModel):
    """Base user model."""

    username: str
    email: str


class UserRegister(UserBase):
    """Extra data needed when adding a new user."""

    password: str


class UserDB(UserBase):
    """User Model as stored in the DB."""

    disabled: bool
    hashed_password: str

    @classmethod
    def get(cls, user_coll: pym_coll.Collection, username: str) -> UserDB:
        """Fetches a user from the DB."""
        user_dict: Optional[dict] = user_coll.find_one({"_id": username})
        if not user_dict:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="Can't fetch user, username not found in the DB.",
            )
        user_db = cls(**user_dict)
        return user_db

    def add(self, user_coll: pym_coll.Collection) -> pym_res.InsertOneResult:
        """Adds a new user to the DB."""
        try:
            result = user_coll.insert_one({**self.dict(), **{"_id": self.username}})
        except pym_err.DuplicateKeyError as exc:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_409_CONFLICT,
                detail="Can't create user, it already exists in the DB.",
            ) from exc
        else:
            return result
