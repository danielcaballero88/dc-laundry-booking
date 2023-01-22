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


def parse_date_to_datetime(date: dt.date) -> dt.datetime:
    """Parse a date to datetime assuming time 00:00."""
    return dt.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
    )


def get_week_dates(target_datetime: dt.datetime, offset: int = 0) -> list[dt.date]:
    """Get the dates of a week from a date."""
    week_starting_date = (
        target_datetime.date()
        - dt.timedelta(days=target_datetime.weekday())
        + dt.timedelta(days=7 * offset)
    )

    week_dates = [week_starting_date]
    for n_days in range(1, 7):
        date = week_starting_date + dt.timedelta(days=n_days)
        week_dates.append(date)

    return week_dates
