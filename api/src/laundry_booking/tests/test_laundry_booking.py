"""Tests for the laundry_booking module."""
import datetime as dt

import pytest

from laundry_booking import lb_types as lbt

from .data.data_laundry_booking import TEST_DATA


class TestLaundryBooking:
    def __init__(self) -> None:
        """Instantiate the test class by parsing the test data."""
        self.user_id = TEST_DATA["example"]["user_id"]
        self.target_datetime = TEST_DATA["example"]["datetime"]
        self.expected_result = TEST_DATA["example"]["result"]

    def parse_bookings(self) -> None:
        """Parse the bookings from the test data into the correct format."""
        booked_by_others: lbt.SlotsTakenDict = {}
        booked_by_user: lbt.SlotsTakenDict = {}

        for test_user_id, test_user_dict in TEST_DATA["users"].items():
            for date_str, slot_id in test_user_dict.items():
                date = dt.datetime.strptime(date_str, "%Y-%m-%d")
                if test_user_id == self.user_id:
                    self.assign_taken_slot(booked_by_user, date, slot_id)
                else:
                    self.assign_taken_slot(booked_by_others, date, slot_id)

    @staticmethod
    def assign_taken_slot(
        taken_slots: lbt.SlotsTakenDict, date: dt.date, slot_id: lbt.SlotIdInt
    ):
        """Assign a taken slot in a given date to a SlotsTakenDict.

        This is done avoiding KeyError if the date is not yet in the dict.
        """
        if date not in taken_slots:
            taken_slots[date] = []
        taken_slots[date].append(slot_id)
