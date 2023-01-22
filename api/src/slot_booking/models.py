"""Data models and enums (and custom types) for the Slot Booking package."""
import datetime as dt
import enum as e
import typing as t

SlotIdInt = t.Literal[0, 1, 2, 3, 4]
SlotIdStr = t.Literal["0", "1", "2", "3", "4"]
SlotStatusIdInt = t.Literal[0, 1, 2, 3]

HourInt = t.Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
]

SlotTimesDict = t.TypedDict(
    "SlotTimesDict", {"start_hour": HourInt, "end_hour": HourInt}
)


SlotsTakenDict = dict[dt.date, list[SlotIdInt]]

WeekSlotsDict = dict[dt.date, dict[SlotIdInt, SlotStatusIdInt]]

slots_hours: dict[SlotIdInt, SlotTimesDict] = {
    0: {"start_hour": 7, "end_hour": 10},
    1: {"start_hour": 10, "end_hour": 13},
    2: {"start_hour": 13, "end_hour": 16},
    3: {"start_hour": 16, "end_hour": 19},
    4: {"start_hour": 19, "end_hour": 22},
}


class SlotsStatus(e.Enum):
    """Enum for the statuses that each slot can have."""

    UNAVAILABLE = 0
    AVAILABLE = 1
    BOOKED_BY_OTHER = 2
    BOOKED_BY_USER = 3
