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
        """Executes passed `func` when `Result` is `Success`, otherwise ignores.

        Example::

                Success(3) >> lambda x: Success(x + 1)  # Success(4)
                Failure(3) >> lambda x: Success(x + 1)  # Failure(3)

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
        """Executes passed `func` when `Result` is `Failure`, otherwise ignores.

        Example::

                Success(3) << lambda x: Success(x + 1)  # Success(3)
                Failure(3) << lambda x: Success(x + 1)  # Success(4)

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
    """Container that marks underlying value as `Success`full execution result."""

    value: TSuccess


@dataclasses.dataclass(frozen=True)
class Failure(Result[Any, TFailure]):
    """Container that marks underlying value as `Failure` execution result."""

    value: TFailure


def safe(
    func: Callable[[TSuccess], TSuccess | Exception]
) -> Callable[[TSuccess], Result[TSuccess, Exception]]:
    """When function returns or throws `Exception` it is wrapped into `Failure`.

    Example::

            @safe
            def divide_one_by(x: int) -> int:
                return 1 / x

            divide_one_by(0)  # Failure(value=ZeroDivisionError('division by zero'))

            @safe
            def divide_two_by(x: int) -> int | Exception:
                match x:
                    case 0:
                        return ValueError('Cannot divide by zero')
                    case value:
                        return 2 / value

            divide_two_by(0)  # Failure(value=ValueError('Cannot divide by zero'))

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
