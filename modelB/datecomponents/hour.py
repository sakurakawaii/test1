from typing import Literal, cast, get_args
from .base import NamedNumericDateComponentBase

type StandardHourName = Literal[
    "12am", "1am", "2am", "3am",
    "4am", "5am", "6am", "7am",
    "8am", "9am", "10am", "11am",
    "12pm", "1pm", "2pm", "3pm",
    "4pm", "5pm", "6pm", "7pm",
    "8pm", "9pm", "10pm", "11pm"
]
type SpecialHourName = Literal["midnight", "noon"]

type HourName = StandardHourName | SpecialHourName
type HourValue = HourName | int

class Hour(NamedNumericDateComponentBase[HourName]):
    _NAMES = list(get_args(StandardHourName)) + list(get_args(SpecialHourName))
    _MIN = 0
    _MAX = 23
    _ALIASES = {
        "midnight": "12am",
        "noon": "12pm"
    }

    def to_24h(self) -> int:
        """
        The 24h representation of this hour (0-23). Alias for int_id.
        """
        return self.int_id
    
    def to_12h(self) -> StandardHourName:
        """
        The 12h representation of this hour (e.g. "1pm"). Alias for str_id,
        but cast to StandardHourName to exclude the special aliases "midnight" and "noon"
        which cannot actually appear as str_id since they are registered as aliases.
        """
        return cast(StandardHourName, self.str_id)