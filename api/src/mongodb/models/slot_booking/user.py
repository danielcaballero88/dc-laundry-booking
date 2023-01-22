"""Module to interact with the "slot_booking.user" collection.

The collection is assigned to the slot_booking.SlotBookingManager class on
initialization and it's not necessarily "auth.user", but it can be any desired database
and collection can be used.
"""

from __future__ import annotations

import typing as t

import fastapi as fa
import pydantic as pyd
import pymongo.collection as pym_coll
import pymongo.results as pym_res

from src.slot_booking import models as lb_m
from src.slot_booking.utils import datetime_utils as lb_dp


class UserAdd(pyd.BaseModel):
    """Model to add a user to the Slot Booking DB."""

    appartment: int
    name: str
    bookings: dict[str, lb_m.SlotIdInt]

    def upsert(
        self, user_coll: pym_coll.Collection, username: str
    ) -> pym_res.UpdateResult:
        """Add a new user to the DB."""
        obj = {**self.dict(), **{"_id": username}}
        result = user_coll.replace_one({"_id": obj["_id"]}, obj, upsert=True)
        return result

    @pyd.root_validator(pre=True)
    def add_default_bookings_empty(cls, values: dict) -> dict:
        """Adds an empty dict as default value for bookings."""
        if "bookings" not in values:
            values["bookings"] = {}
        return values


class User(UserAdd):
    """Model to interact with a user of the Slot Booking DB."""

    def upsert(self, *args, **kwargs):
        """Override parent class 'upsert' method to make it invalid for this class."""
        raise NotImplementedError(
            "Not allowed to directly add or modify Slot Booking users."
        )

    @classmethod
    def get(cls, user_coll: pym_coll.Collection, username: str) -> User:
        """Fetch a user from the DB."""
        user_dict: t.Optional[dict] = user_coll.find_one({"_id": username})
        if not user_dict:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="User data not found in the Slot Booking DB.",
            )
        user_db = cls(**user_dict)
        return user_db

    def add_booking(
        self,
        user_coll: pym_coll.Collection,
        username: str,
        date_str: str,
        slot_id: lb_m.SlotIdInt,
    ) -> pym_res.UpdateResult:
        """Add a booking to a user in the DB."""
        update_one_result = user_coll.update_one(
            {
                "_id": username,
                f"bookings.{date_str}": {"$exists": False},
            },
            {"$set": {f"bookings.{date_str}": slot_id}},
        )
        return update_one_result

    def delete_booking(
        self,
        user_coll: pym_coll.Collection,
        username: str,
        date_str: str,
        slot_id: lb_m.SlotIdInt,
    ) -> pym_res.UpdateResult:
        """Delete a booking of the user in the DB."""
        result = user_coll.update_one(
            {
                "_id": username,
                f"bookings.{date_str}": {"$exists": True},
            },
            {
                "$unset": {f"bookings.{date_str}": ""},
            },
        )
        return result

    def get_bookings(self) -> lb_m.SlotsTakenDict:
        """Get the bookings made by the user."""
        bookings_by_user: lb_m.SlotsTakenDict = {}
        for date_str, slot_id in self.bookings.items():
            date = lb_dp.parse_date_from_string(date_str)
            bookings_by_user[date] = [slot_id]
        return bookings_by_user

    def get_bookings_by_others(
        self,
        user_coll: pym_coll.Collection,
        username: str,
    ) -> lb_m.SlotsTakenDict:
        """Get the bookings of other users."""
        docs = user_coll.find({"_id": {"$ne": username}}, {"bookings": 1, "_id": 0})
        bookings_by_others: lb_m.SlotsTakenDict = {}
        for doc in docs:
            for date_str, slot_id in doc["bookings"].items():
                date = lb_dp.parse_date_from_string(date_str)
                if date not in bookings_by_others:
                    bookings_by_others[date] = []
                bookings_by_others[date].append(slot_id)

        return bookings_by_others
