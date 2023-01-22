"""Test data for the laundry_booking module."""

TEST_DATA: dict = {
    "slots": {
        "slots_enum": {
            # <slot_id>: "<hour_start>-<hour_end>"
            0: "7-10",
            1: "10-13",
            2: "13-16",
            3: "16-19",
            4: "19-22",
        },
        "status_enum": {
            # <status_id>: <status_description>
            0: "unavailable",  # This can be due to being a past slot, or being unavailable for maintenance or whatever reasons. Not booked by anyone.
            1: "available",  # Present or future slot that is not yet booked by anyone.
            2: "booked by other",  # Present or future slot that is booked by someone else than the current user.
            3: "booked by user",  # Present or future slot that is booked by the current user.
        },
    },
    "users": {
        # <username[unique]>: <user_obj>
        "dan": {
            "appartment": 1101,
            "name": "Daniel Caballero",
            "bookings": {
                "2022-12-07": 1,
            },
        },
        "cosful123": {
            "appartment": 1101,
            "name": "Cosme Fulanito",
            "bookings": {
                # <date>: <slot_id> -> Each user can only have one booking per date, and three in total at any given time.
                "2022-12-06": 3,
                "2022-12-11": 2,
            },
        },
        # ... more users with potentially more bookings
    },
    "example": {
        "description": "The date is 2022-12-06 at 9:55am, previous slots are unavailable because they are passed, and some bookings are made above. User 'dan' receives the following result when trying to book a slot. Note that the 10am slot is available because 1) there are no bookings from other users 2) dan still has a booking available to make this week (infinite bookings at the moment, need to impement some restrictions later on to avoid one user from booking all slots) and 3) a slot becomes unavailable only after the start time if not booked.",
        "username": "dan",
        "datetime": "2022-12-06 09:55",
        "result": {
            "2022-12-05": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
            "2022-12-06": {0: 0, 1: 1, 2: 1, 3: 2, 4: 1},
            "2022-12-07": {0: 1, 1: 3, 2: 1, 3: 1, 4: 1},
            "2022-12-08": {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
            "2022-12-09": {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
            "2022-12-10": {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
            "2022-12-11": {0: 1, 1: 1, 2: 2, 3: 1, 4: 1},
        },
    },
}
