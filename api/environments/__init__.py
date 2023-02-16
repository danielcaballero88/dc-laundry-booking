import os

ENV = os.environ.get("DC_SLOT_BOOKING_ENV")

from .base import *

if ENV == "development":
    from .development import *
