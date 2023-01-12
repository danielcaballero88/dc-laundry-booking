"""Module with utilities for date parsing."""
import datetime as dt


def parse_date_from_string(
    date_str: str, format_specifier: str = "%Y-%m-%d"
) -> dt.date:
    """Parse a date from a string to a date object."""
    return dt.datetime.strptime(date_str, format_specifier).date()


def parse_datetime_from_string(
    datetime_str: str, format_specifier: str = "%Y-%m-%d %H:%M"
) -> dt.datetime:
    """Parse a datetime from a string to a datetime object."""
    return dt.datetime.strptime(datetime_str, format_specifier)
