"""Module to interact with the "laundry_booking.user" collection.

The collection is assigned to the laundry_booking.LaundryBookingManager class on
initialization and it's not necessarily "auth.user", but it can be any desired database
and collection can be used.
"""

from __future__ import annotations

from typing import Optional

import fastapi as fa
import pydantic as pyd
import pymongo.collection as pym_coll
import pymongo.results as pym_res


class UserAdd(pyd.BaseModel):
    """Model to add a user to the Laundry Booking DB."""

    appartment: int
    name: str

    def upsert(
        self, user_coll: pym_coll.Collection, username: str
    ) -> pym_res.UpdateResult:
        """Add a new user to the DB."""
        obj = {**self.dict(), **{"_id": username}}
        result = user_coll.replace_one({"_id": obj["_id"]}, obj, upsert=True)
        return result


class User(UserAdd):
    """Model to interact with a user of the Laundry Booking DB."""

    bookings: dict[str, int]

    def upsert(self, *args, **kwargs):
        """Override parent class 'upsert' method to make it invalid for this class."""
        raise NotImplementedError(
            "Not allowed to directly add or modify Laundry Booking users."
        )

    @classmethod
    def get(cls, user_coll: pym_coll.Collection, username: str) -> User:
        """Fetch a user from the DB."""
        user_dict: Optional[dict] = user_coll.find_one({"_id": username})
        if not user_dict:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="User data not found in the Laundry Booking DB.",
            )
        user_db = cls(**user_dict)
        return user_db
