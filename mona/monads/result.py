import abc
import dataclasses
import functools
from typing import Any, Callable, Generic, TypeVar

from mona.monads.core import Alterable, Bindable

TSuccess = TypeVar("TSuccess")
TFailure = TypeVar("TFailure")


@dataclasses.dataclass(frozen=True)
class Result(Bindable, Alterable, Generic[TSuccess, TFailure], abc.ABC):
    """Base abstract container for computation `Result`.

    Railway-oriented programming concept. Stands for `Result` of some computation
    sequence. Can be of 2 types: `Success` and `Failure`.
    """

    value: TSuccess | TFailure

    def __rshift__(
        self, func: Callable[[TSuccess], "Result[TSuccess, TFailure]"]
    ) -> "Result[TSuccess, TFailure]":
        """Binding.

        Args:
            func (Callable[[TSuccess], Result[TSuccess, TFailure]]): to bind to
            container

        Returns:
            Result[TSuccess, TFailure]: of binding
        """
        match self:
            case Success(value):
                return func(value)
            case Failure() as failure:
                return failure

    def __lshift__(
        self, func: Callable[[TFailure], "Result[TSuccess, TFailure]"]
    ) -> "Result[TSuccess, TFailure]":
        """Altering.

        Args:
            func (Callable[[TFailure], &quot;Result[TSuccess, TFailure]&quot;]):
            _description_

        Returns:
            Result[TSuccess, TFailure]: _description_
        """
        match self:
            case Success() as success:
                return success
            case Failure(value):
                return func(value)


@dataclasses.dataclass(frozen=True)
class Success(Result[TSuccess, Any]):
    """Success."""

    value: TSuccess


@dataclasses.dataclass(frozen=True)
class Failure(Result[Any, TFailure]):
    """Failure."""

    value: TFailure


def bind(
    func: Callable[[TSuccess], Result[TSuccess, TFailure]],
    cnt: Result[TSuccess, TFailure],
) -> Result[TSuccess, TFailure]:
    """Binding.

    Args:
        func (Callable[[TSuccess], Result[TSuccess, TFailure]]): _description_
        cnt (Result[TSuccess, TFailure]): _description_

    Returns:
        Result[TSuccess, TFailure]: _description_
    """
    return cnt >> func


def alt(
    func: Callable[[TFailure], Result[TSuccess, TFailure]],
    cnt: Result[TSuccess, TFailure],
) -> Result[TSuccess, TFailure]:
    """Altering.

    Args:
        func (Callable[[TFailure], Result[TSuccess, TFailure]]): _description_
        cnt (Result[TSuccess, TFailure]): _description_

    Returns:
        Result[TSuccess, TFailure]: _description_
    """
    return cnt << func


def safe(
    func: Callable[[TSuccess], TSuccess | Exception]
) -> Callable[[TSuccess], Result[TSuccess, Exception]]:
    """When function returns or throws `Exception` it is wrapped into `Failure`.

    Args:
        func (Callable[[TSuccess], TSuccess | Exception]): _description_

    Returns:
        Callable[[TSuccess], Result[TSuccess, Exception]]: _description_
    """

    @functools.wraps(func)
    def _wrapper(value: TSuccess):
        try:
            match func(value):
                case Exception() as error:
                    return Failure(error)
                case value:
                    return Success(value)
        except Exception as error:
            return Failure(error)

    return _wrapper
