import pytest
from typing import Any
from abc import ABC, abstractmethod

class Mixin(ABC): 
    @abstractmethod
    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        """
        The core method that tests a positive condition. It should
        intercept a particular `feature` value and run its condition, but
        leave non-intercepted features up to `super` to see if the next class
        in the MRO can handle it.

        Add arguments to allow injecting fixtures into the condition.
        """
        raise NotImplementedError(f"No condition defined for the feature {feature}")

    def validate(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        """
        The method that defined test methods should directly call. It will call the `condition` method and invert the result if `negative` is True.
        """

        result: bool = False

        expected_exceptions: tuple[type[BaseException], ...]

        fail_for_feature: bool | type[BaseException] | tuple[type[BaseException], ...] = getattr(self, f"fail_{feature}", False)
        negative_for_feature: bool = getattr(self, f"negative_{feature}", False)

        if fail_for_feature is not False:
            if fail_for_feature is True:
                    expected_exceptions = (BaseException,)
            elif isinstance(fail_for_feature, tuple):
                expected_exceptions = fail_for_feature
            elif fail_for_feature is not False:
                expected_exceptions = (fail_for_feature,)

            with pytest.raises(expected_exceptions):
                result = self.condition(feature, *args, **kwargs)
        else:
            result = self.condition(feature, *args, **kwargs)
            

        if negative_for_feature:
            return not result
        else:
            return result
