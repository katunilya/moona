from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Generic, TypeVar

from mona.monads.core import Alterable, Bindable

TSuccess = TypeVar("TSuccess")
TFailure = TypeVar("TFailure")
VSuccess = TypeVar("VSuccess")
VFailure = TypeVar("VFailure")


@dataclass(frozen=True)
class Result(Bindable, Alterable, Generic[TSuccess, TFailure], ABC):
    """Base abstract container for computation `Result`.

    Railway-oriented programming concept. Stands for `Result` of some computation
    sequence. Can be of 2 types: `Success` and `Failure`.

    Example::

        def make_moderator_admin(id: int) -> Result[User, Exception]:
            return (
                get_user(id)
                >> check_user_role_is('moderator')
                >> set_user_role('admin')
                >> update_user
            )

    """

    value: TSuccess | TFailure

    def __rshift__(
        self, func: Callable[[TSuccess], "Result[VSuccess, VFailure]"]
    ) -> "Result[VSuccess, VFailure]":
        match self:
            case Success(value):
                return func(value)
            case Failure() as failure:
                return failure

    def __lshift__(
        self, func: Callable[[TFailure], "Result[VSuccess, VFailure]"]
    ) -> "Result[VSuccess, VFailure]":
        match self:
            case Success() as success:
                return success
            case Failure(value):
                return func(value)

    @staticmethod
    def bound(
        func: Callable[[TSuccess], "Result[VSuccess, VFailure]"],
    ) -> Callable[["Result[TSuccess, TFailure]"], "Result[VSuccess, VFailure]"]:
        """Decorator for functions that will be executed only with `Success` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.bindable
            def check_is_admin(user: User) -> User:
                ...

            result = check_is_admin(Success(User(..)))  # Result[User, Exception]
        """

        @wraps(func)
        def _bound(cnt: "Result[TSuccess, TFailure]") -> "Result[TSuccess, TFailure]":
            return cnt >> func

        return _bound

    @staticmethod
    def altered(
        func: Callable[[TFailure], "Result[VSuccess, VFailure]"],
    ) -> Callable[["Result[TSuccess, TFailure]"], "Result[VSuccess, VFailure]"]:
        """Decorator for functions that will be executed only with `Failure` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.bindable
            def handle_error(err: Exception) -> str:
                ...

            result = handle_error(Failure(Exception(..)))  # Success[str]
        """

        @wraps(func)
        def _altered(cnt: "Result[TSuccess, TFailure]") -> "Result[TSuccess, TFailure]":
            return cnt << func

        return _altered

    @staticmethod
    def safe(
        func: Callable[[TSuccess], VSuccess | Exception]
    ) -> Callable[[TSuccess], Result[VSuccess, Exception]]:
        """When function returns or throws `Exception` it is wrapped into `Failure`.

        Example::

                @Result.safe
                def divide_one_by(x: int) -> int:
                    return 1 / x

                divide_one_by(0)  # Failure(value=ZeroDivisionError('division by zero'))

                @Result.safe
                def divide_two_by(x: int) -> int | Exception:
                    match x:
                        case 0:
                            return ValueError('Cannot divide by zero')
                        case value:
                            return 2 / value

                divide_two_by(0)  # Failure(value=ValueError('Cannot divide by zero'))
        """

        @wraps(func)
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

    @staticmethod
    def successfull(value: TSuccess) -> Success[TSuccess]:
        """Wraps passed value into Success container.

        Args:
            value (TSuccess): value to wrap.

        Returns:
            Success[TSuccess]: container.
        """
        return Success(value)

    @staticmethod
    def failed(value: TFailure) -> Failure[TFailure]:
        """Wraps passed value into Failure container.

        Args:
            value (TFailure): value to wrap.

        Returns:
            Failure[TFailure]: container.
        """
        return Failure(value)

    @staticmethod
    def safely_bound(
        func: Callable[[TSuccess], VSuccess | Exception]
    ) -> Callable[[Result[TSuccess, TFailure]], Result[VSuccess, Exception]]:
        """Decorator for functions that combines `bound` and `safe`."""
        return Result.bound(Result.safe(func))


@dataclass(frozen=True)
class Success(Result[TSuccess, Any]):
    """Container that marks underlying value as `Success`full execution result."""

    value: TSuccess


@dataclass(frozen=True)
class Failure(Result[Any, TFailure]):
    """Container that marks underlying value as `Failure` execution result."""

    value: TFailure


Safe = Result[TSuccess, Exception]
