from __future__ import annotations # So that classes can self-reference
from typing import Any, ClassVar, Generic, TypeVar, cast, Self
NameT = TypeVar("NameT", bound=str)

class NumericDateComponentBase:
    """
    Base class providing numeric range logic for date components.
    Subclasses must define _MIN and _MAX.
    """

    _MIN: ClassVar[int] = 0
    _MAX: ClassVar[int] = 0

    _int_id: int

    def __init__(self, value: int):
        self._int_id = self.normalize_int(value)

    @property
    def int_id(self) -> int:
        return self._int_id

    @int_id.setter
    def int_id(self, value: int):
        self._int_id = self.normalize_int(value)

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return self.int_id == cast(NumericDateComponentBase, other).int_id

    def __hash__(self) -> int:
        return hash(self.int_id)
    
    @classmethod
    def create_from(cls, value: Self | int) -> Self:
        if type(value) is int:
            return cls(value)
        
        # Create a copy with the same int_id
        return cls(int(value))

    @classmethod
    def size(cls) -> int:
        """Returns the number of valid values for this date component."""
        return cls._MAX - cls._MIN

    @classmethod
    def normalize_int(cls, value: int) -> int:
        """
        Normalizes an input to its integer representation.
        Integers are silently clamped.
        """
        if type(value) is int:  # Using type() to avoid treating bools as ints
            return max(cls._MIN, min(value, cls._MAX))
        raise TypeError(f"Expected int, got {type(value).__name__}")

    @classmethod
    def argtype(cls, value: str):
        """
        To be used with argparse. Takes an input,
        detects if it's an integer and converts it
        if so, then normalizes it.
        """
        try:
            return cls.normalize_int(int(value))
        except ValueError:
            raise ValueError(f"Invalid {cls.__name__.lower()} value: '{value}'")

    def _apply_loop(self, loop_count: int) -> Self:
        """
        Override to respond to looping around the end or beginning of the range as appropriate.
        By default, this does nothing. Should always receive a non-zero number, but it may be
        positive or negative depending on the direction of the loop.
        """
        return self

    def __add__(self, delta: int) -> Self:
        """
        Adds a delta to this date component, returning a new instance.
        Handles looping around the end or beginning of the range as appropriate.
        """
        normal_int = self.int_id - self._MIN + delta # Convert to 0-based for easier modulo arithmetic
        loop_count = normal_int // self.size()
        wrapped_int = (normal_int % self.size()) + self._MIN
        
        result = type(self)(wrapped_int)
        if loop_count != 0: # Only apply looping logic if we actually looped around, to avoid unnecessary adjustments
            result = result._apply_loop(loop_count)
        
        return result

    def __sub__(self, delta: int) -> Self:
        """
        Subtracts a delta from this date component, returning a new instance.
        Handles looping around the end or beginning of the range as appropriate.
        """
        return self.__add__(-delta)

    def __int__(self) -> int:
        return self.int_id


class NamedNumericDateComponentBase(NumericDateComponentBase, Generic[NameT]):
    """
    Base class providing shared normalization logic for date components.
    Subclasses must define _NAMES, _MIN, and _MAX.
    """

    _NAMES: ClassVar[list[str]] = []
    _LOOKUP: ClassVar[dict[str, int]] = {}
    _ALIASES: ClassVar[dict[str, str]] = {}

    _str_id: NameT

    def __init__(self, value: int | NameT):
        int_val = self.normalize_int(value)
        super().__init__(int_val)
        self._str_id = self.normalize_str(int_val)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        alias_keys = {alias.lower() for alias in cls._ALIASES}
        cls._NAMES = [name for name in cls._NAMES if name.lower() not in alias_keys]
        cls._LOOKUP = {name.lower(): i + cls._MIN for i, name in enumerate(cls._NAMES)}

    # Redefine int_id setter to keep _str_id in sync
    @property
    def int_id(self) -> int:
        return self._int_id

    @int_id.setter
    def int_id(self, value: int):
        int_id = self.normalize_int(value)
        self._int_id = int_id
        self._str_id = self.normalize_str(int_id)

    @property
    def str_id(self) -> NameT:
        return self._str_id

    @str_id.setter
    def str_id(self, value: NameT):
        str_id = self.normalize_str(value)
        int_id = self.normalize_int(str_id)
        self._int_id = int_id
        self._str_id = str_id

    @classmethod
    def _maybe_resolve_alias(cls, value: str) -> str:
        low_value = value.lower()
        if low_value in cls._ALIASES:
            return cls._ALIASES[low_value]
        return low_value
    
    @classmethod
    def create_from(cls, value: Self | int | NameT) -> Self: # type: ignore[override]
        if isinstance(value, str):
            return cls(cast(NameT, value))
        
        return super().create_from(value)

    @classmethod
    def normalize_int(cls, value: int | NameT) -> int:
        """
        Normalizes an input to its integer representation.
        Strings are matched case-insensitively. Integers are silently clamped.
        """
        if isinstance(value, str):
            low_value = cls._maybe_resolve_alias(value)
            if low_value not in cls._LOOKUP:
                raise ValueError(f"Invalid {cls.__name__.lower()} name: '{value}'")
            return cls._LOOKUP[low_value]
        return super().normalize_int(value)

    @classmethod
    def normalize_str(cls, value: int | NameT) -> NameT:
        """
        Normalizes an input to its string representation.
        Integers are clamped before conversion. Strings are
        validated and returned in their canonical form.
        """
        if type(value) is int:
            clamped = max(cls._MIN, min(value, cls._MAX))
            return cast(NameT, cls._NAMES[clamped - cls._MIN])

        if isinstance(value, str):
            low_value = cls._maybe_resolve_alias(value)
            if low_value not in cls._LOOKUP:
                raise ValueError(f"Invalid {cls.__name__.lower()} name: '{value}'")
            return cast(NameT, cls._NAMES[cls._LOOKUP[low_value] - cls._MIN])

        raise TypeError(f"Expected int or str, got {type(value).__name__}")

    @classmethod
    def argtype(cls, value: str) -> int | NameT:  # type: ignore[override]
        """
        To be used with argparse. Takes an input,
        detects if it's an integer and converts it
        if so, then normalizes it.
        """
        try:
            int_value = int(value)
            return cls.normalize_int(int_value)
        except ValueError:
            return cls.normalize_str(cast(NameT, value))

    def __str__(self) -> str:
        return self.str_id
