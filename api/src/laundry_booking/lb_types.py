"""Types for the Laundry Booking package."""
import datetime as dt
import typing as t

SlotIdInt = t.Literal[0, 1, 2, 3, 4]
SlotStatusIdInt = t.Literal[0, 1, 2, 3]

HourInt = t.Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
]

SlotTimesDict = t.TypedDict(
    "SlotTimesDict", {"start_hour": HourInt, "end_hour": HourInt}
)

SlotsTakenDict = dict[dt.date, list[SlotIdInt]]

WeekSlotsDict = dict[dt.date, dict[SlotIdInt, SlotStatusIdInt]]
