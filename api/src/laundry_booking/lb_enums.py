"""Enums for the Laundry Booking package."""
import enum as e
import typing as t

from laundry_booking import lb_types as lbt


# Slots times should eventually come from the DB if desired to be changed easily.
class SlotTimesDict(t.TypedDict):
    """Dictionary for the slot times data."""

    start_time: lbt.HourInt
    end_time: lbt.HourInt


slots_times: dict[lbt.SlotIdInt, SlotTimesDict] = {
    0: {"start_time": 7, "end_time": 10},
    1: {"start_time": 10, "end_time": 13},
    2: {"start_time": 13, "end_time": 16},
    3: {"start_time": 16, "end_time": 19},
    4: {"start_time": 19, "end_time": 22},
}


class SlotsStatus(e.Enum):
    """Enum for the statuses that each slot can have."""

    UNAVAILABLE = 0
    AVAILABLE = 1
    BOOKED_BY_OTHER = 2
    BOOKED_BY_USER = 3
