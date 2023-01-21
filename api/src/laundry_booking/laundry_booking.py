"""Package with the Laundry Booking logic."""
import copy
import datetime as dt
import typing as t

from . import models as m
from .utils import datetime_utils as dt_u


class LaundryBookingManager:
    """Manager of the laundry room.

    The manager parses the date and slots information for a given week, according to the
    given information about currently unavailable and booked slots for the concerning
    dates.
    """

    def __init__(
        self,
        target_datetime: dt.datetime,
        offset: int = 0,
        slots_unavailable: t.Optional[m.SlotsTakenDict] = None,
        slots_booked_by_others: t.Optional[m.SlotsTakenDict] = None,
        slots_booked_by_user: t.Optional[m.SlotsTakenDict] = None,
    ):
        self.target_datetime = target_datetime
        self.offset = offset
        self.slots_unavailable = slots_unavailable
        self.slots_booked_by_others = slots_booked_by_others
        self.slots_booked_by_user = slots_booked_by_user
        self.week_dates = dt_u.get_week_dates(target_datetime, offset)
        self.week_slots = self.get_week_slots()

    def get_week_slots(self) -> m.WeekSlotsDict:
        """Get the week slots with their statuses."""
        # TODO (dancab 2023-01-03): Improve efficiency of this code.
        # At the moment the complexity is O(nxm) because I go over the dates and then
        # the slots. But since both n and m are small (n=dates=7, m=slots=4) then it's
        # not a critical improvement at the moment.

        # Initialize week_slots dict with all slots available.
        week_slots: m.WeekSlotsDict = {}
        for date in self.week_dates:
            week_slots[date] = {}
            for slot_id in m.slots_hours:
                week_slots[date][slot_id] = m.SlotsStatus.AVAILABLE.value

        # Set correct status for already booked slots.
        if self.slots_booked_by_user:
            week_slots = self.assign_slots_statuses(
                week_slots=week_slots,
                taken_slots=self.slots_booked_by_user,
                taken_status=m.SlotsStatus.BOOKED_BY_USER.value,
            )
        if self.slots_booked_by_others:
            week_slots = self.assign_slots_statuses(
                week_slots=week_slots,
                taken_slots=self.slots_booked_by_others,
                taken_status=m.SlotsStatus.BOOKED_BY_OTHER.value,
            )

        # Set the correct status for unavailable slots, also adding the
        # past slots as unavailable.
        slots_past: m.SlotsTakenDict = {}

        for date, date_slots in week_slots.items():
            if date > self.target_datetime.date():
                # Don't use 'break' because not sure if the dates are
                # looped in order.
                continue
            slots_past[date] = []

            for slot_id in date_slots:
                slot_start_datetime = dt.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=m.slots_hours[slot_id]["start_hour"],
                )
                if slot_start_datetime > self.target_datetime:
                    # Don't use 'break' because not sure if the slot ids
                    # are looped in order.
                    continue
                else:
                    slots_past[date].append(slot_id)

        all_slots_unavailable: m.SlotsTakenDict = {}
        if not self.slots_unavailable:
            all_slots_unavailable = slots_past
        else:
            for date in week_slots:
                # Append both lists of slots (past and unavailable) into
                # a single list. There may be repeated slots but it
                # isn't critical to avoid that at the moment.
                all_slots_unavailable[date] = (
                    slots_past[date] + self.slots_unavailable[date]
                )

        if all_slots_unavailable:
            week_slots = self.assign_slots_statuses(
                week_slots=week_slots,
                taken_slots=all_slots_unavailable,
                taken_status=m.SlotsStatus.UNAVAILABLE.value,
            )

        # That's it.
        return week_slots

    @staticmethod
    def assign_slots_statuses(
        week_slots: m.WeekSlotsDict,
        taken_slots: m.SlotsTakenDict,
        taken_status: m.SlotStatusIdInt,
    ) -> m.WeekSlotsDict:
        """Assign correct status to week slots."""
        # Start with a copy of the input week slots.
        result_week_slots: m.WeekSlotsDict = copy.deepcopy(week_slots)
        # Go over the dates and see if any date has taken slots.
        for date in week_slots:
            if date in taken_slots:
                # If so, go over the taken slots and assign the correct status to them.
                for slot_id in taken_slots[date]:
                    result_week_slots[date][slot_id] = taken_status
        # And return the modified copy.
        return result_week_slots
