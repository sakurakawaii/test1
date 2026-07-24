"""
Project-specific test helpers.

The shipped named component classes (Month, Weekday, Season, Hour) are
unusable as-is: `typing.get_args` on a PEP 695 ``type`` alias returns ``()``,
so their `_NAMES` lists are empty and *every* instantiation fails (see
REPORT.md, defect D1). Subclassing with an explicit `_NAMES` list is the
documented extension point of `NamedNumericDateComponentBase` ("Subclasses
must define _NAMES, _MIN, and _MAX"), so these `Fixed*` subclasses re-supply
*only* the broken class attribute and inherit every piece of behavior under
test. All standard tests for named components run against these.
"""
from dateutils.month import Month
from dateutils.weekday import Weekday
from dateutils.season import Season
from dateutils.hour import Hour

MONTH_NAMES: list[str] = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]
WEEKDAY_NAMES: list[str] = [
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
]
SEASON_NAMES: list[str] = ["spring", "summer", "autumn", "winter", "fall"]
HOUR_NAMES: list[str] = [
    "12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am",
    "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm",
    "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm",
    "midnight", "noon",  # filtered out by __init_subclass__ (registered aliases)
]


class FixedMonth(Month):
    """Month with the intended 12 names restored; all logic inherited."""
    _NAMES = MONTH_NAMES


class FixedWeekday(Weekday):
    """Weekday with the intended 7 names restored; all logic inherited."""
    _NAMES = WEEKDAY_NAMES


class FixedSeason(Season):
    """Season with the intended 5 names (incl. 'fall' alias) restored."""
    _NAMES = SEASON_NAMES


class FixedHour(Hour):
    """Hour with the intended 26 names (incl. special aliases) restored."""
    _NAMES = HOUR_NAMES
