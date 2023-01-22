"""Tests for the slot_booking module."""
import datetime as dt

import pytest  # pylint: disable=unused-import

from .. import slot_booking as lb
from .. import models as lbm
from ..utils import datetime_utils as dt_u
from .data.data_slot_booking import TEST_DATA


class ParsedTestData:
    """Class to parse and store the test data."""

    def __init__(self) -> None:
        """Instantiate the test class by parsing the test data."""
        self.username = TEST_DATA["example"]["username"]
        target_datetime_str = TEST_DATA["example"]["datetime"]
        self.target_datetime = dt_u.parse_datetime_from_string(target_datetime_str)
        self.expected_result = self.parse_expected_result(
            TEST_DATA["example"]["result"]
        )
        self.booked_by_others, self.booked_by_user = self.parse_bookings()

    def parse_expected_result(self, raw_expected_resuslt: dict) -> lbm.WeekSlotsDict:
        """Parse the expected result to the correct format."""
        parsed_expected_result: lbm.WeekSlotsDict = {}
        for date_str, date_slots_dict in raw_expected_resuslt.items():
            date = dt_u.parse_date_from_string(date_str)
            parsed_expected_result[date] = date_slots_dict
        return parsed_expected_result

    def parse_bookings(self) -> tuple[lbm.SlotsTakenDict, lbm.SlotsTakenDict]:
        """Parse the bookings from the test data into the correct format."""
        booked_by_others: lbm.SlotsTakenDict = {}
        booked_by_user: lbm.SlotsTakenDict = {}

        for test_username, test_user_dict in TEST_DATA["users"].items():
            test_user_bookings = test_user_dict.get("bookings", {})
            for date_str, slot_id in test_user_bookings.items():
                date = dt_u.parse_date_from_string(date_str)
                if test_username == self.username:
                    self.assign_taken_slot(booked_by_user, date, slot_id)
                else:
                    self.assign_taken_slot(booked_by_others, date, slot_id)

        return booked_by_others, booked_by_user

    @staticmethod
    def assign_taken_slot(
        taken_slots: lbm.SlotsTakenDict, date: dt.date, slot_id: lbm.SlotIdInt
    ):
        """Assign a taken slot in a given date to a SlotsTakenDict.

        This is done avoiding KeyError if the date is not yet in the dict.
        """
        if date not in taken_slots:
            taken_slots[date] = []
        taken_slots[date].append(slot_id)


def test_slot_booking_manager():
    "Test the SlotBookingManager class."
    parsed_test_data = ParsedTestData()
    slot_booking_manager = lb.SlotBookingManager(
        target_datetime=parsed_test_data.target_datetime,
        offset=0,
        slots_booked_by_others=parsed_test_data.booked_by_others,
        slots_booked_by_user=parsed_test_data.booked_by_user,
    )
    assert slot_booking_manager.week_slots == parsed_test_data.expected_result
