from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Any, Awaitable, Callable, Generator, Generic, TypeVar

from mona.monads.core import Alterable, Bindable

TOk = TypeVar("TOk")
TBad = TypeVar("TBad")
VOk = TypeVar("VOk")
VBad = TypeVar("VBad")


@dataclass(frozen=True, slots=True)
class FutureResult(Generic[TOk, TBad], ABC):
    """Container for async `Result`.

    Works with both sync and async functions.

    Example::

            result: Result = await (
                FutureResult(get_user_async(id))
                .then(if_user_role("moderator"))
                .then(set_user_role("admin"))
                .then_future(update_user_async)
            )
    """

    value: Awaitable[Result[TOk, TBad]]

    def __await__(self) -> Generator[None, None, Result[TOk, TBad]]:
        return self.value.__await__()

    async def __then(
        self, func: Callable[[TOk], Result[VOk, VBad]]
    ) -> Result[TOk, TBad]:
        match await self.value:
            case Ok(value):
                return func(value)
            case Bad() as bad:
                return bad

    def then(self, func: Callable[[TOk], Result[VOk, VBad]]) -> FutureResult[TOk, TBad]:
        """Execute sync `func` if async result is `Ok`.

        Args:
            func (Callable[[TOk], Result[VOk, VBad]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__then(func))

    async def __otherwise(
        self, func: Callable[[TBad], Result[VOk, VBad]]
    ) -> Result[VOk, VBad]:
        match await self.value:
            case Bad(value):
                return func(value)
            case Ok() as ok:
                return ok

    def otherwise(
        self, func: Callable[[TBad], Result[VOk, VBad]]
    ) -> FutureResult[TOk, TBad]:
        """Execute sync `func` if async result is `Bad`.

        Args:
            func (Callable[[TBad], Result[VOk, VBad]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__otherwise(func))

    async def __then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VBad]]]
    ) -> Result[TOk, TBad]:
        match await self.value:
            case Ok(value):
                return await func(value)
            case Bad() as bad:
                return bad

    def then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VBad]]]
    ) -> FutureResult[TOk, TBad]:
        """Execute async `func` if async result is `Ok`.

        Args:
            func (Callable[[TOk], Awaitable[Result[VOk, VBad]]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[TBad], Awaitable[Result[VOk, VBad]]]
    ) -> Result[TOk, TBad]:
        match await self.value:
            case Bad(value):
                return await func(value)
            case Ok() as ok:
                return ok

    def otherwise_future(
        self, func: Callable[[TBad], Awaitable[Result[VOk, VBad]]]
    ) -> FutureResult[TOk, TBad]:
        """Execute async `func` if async result if `Bad`..

        Args:
            func (Callable[[TBad], Awaitable[Result[VOk, VBad]]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__otherwise_future(func))

    # TODO if_ok for async function
    # TODO if_bad for async functions
    # TODO returns for async functions
    # TODO excepts for async functions
    # TODO if_ok_returns for async functions
    # TODO if_bad_returns for async functions
    # TODO if_ok_excepts for async functions
    # TODO if_bad_excepts for async functions


@dataclass(frozen=True, slots=True)
class Result(Bindable, Alterable, Generic[TOk, TBad], ABC):
    """Base abstract container for computation `Result`.

    Railway-oriented programming concept. Stands for `Result` of some computation
    sequence. Can be of 2 types: `Success` and `Failure`.

    Example::

        def make_moderator_admin(id: int) -> Result[User, Exception]:
            return (
                get_user(id)
                .then(check_user_role_is('moderator'))
                .then(set_user_role('admin'))
                .then(update_user)
            )
    """

    value: TOk | TBad

    def then(self, func: Callable[[TOk], Result[VOk, VBad]]) -> Result[VOk, VBad]:
        """Binding for sync function that handle `Ok`.

        Executes passed function only when container is `Ok`, otherwise just returns
        container.

        Args:
            func (Callable[[TOk], Result[VOk, VBad]]): to execute.

        Returns:
            Result[VOk, VBad]: result of function execution or initial monad container
            if one was `Bad`.
        """
        match self:
            case Ok(value):
                return func(value)
            case Bad() as bad:
                return bad

    def otherwise(self, func: Callable[[TBad], Result[VOk, VBad]]) -> Result[VOk, VBad]:
        """Binding for sync function that handle `Bad`.

        Executes passed function only when container is `Bad`, otherwise just returns
        container.

        Args:
            func (Callable[[TBad], Result[VOk, VBad]]): to execute.

        Returns:
            Result[VOk, VBad]: result if function execution or initial monad container
            if one is `Ok`.
        """
        match self:
            case Bad(value):
                return func(value)
            case Ok() as ok:
                return ok

    async def __then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VBad]]]
    ) -> Result[VOk, VBad]:
        match self:
            case Ok(value):
                return await func(value)
            case Bad() as bad:
                return bad

    def then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VBad]]]
    ) -> FutureResult[VOk, VBad]:
        """Execute async `func` if `Result` value is `Ok` and return `FutureResult`.

        Args:
            func (Callable[[TOk], Awaitable[Result[VOk, VBad]]]): to execute.

        Returns:
            FutureResult[VOk, VBad]: result.
        """
        return FutureResult(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[TBad], Awaitable[Result[VOk, VBad]]]
    ) -> Result[VOk, VBad]:
        match self:
            case Bad(value):
                return await func(value)
            case Ok() as ok:
                return ok

    def otherwise_future(
        self, func: Callable[[TBad], Awaitable[Result[VOk, VBad]]]
    ) -> FutureResult[VOk, VBad]:
        """Execute async `func` if `Result` value is `Bad` and return `FutureResult`.

        Args:
            func (Callable[[TBad], Awaitable[Result[VOk, VBad]]]): to execute.

        Returns:
            FutureResult[VOk, VBad]: result.
        """
        return FutureResult(self.__otherwise_future(func))

    @staticmethod
    def if_ok(
        func: Callable[[TOk], "Result[VOk, VBad]"],
    ) -> Callable[["Result[TOk, TBad]"], "Result[VOk, VBad]"]:
        """Decorator for functions that will be executed only with `Success` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.if_ok
            def check_is_admin(user: User) -> User:
                ...

            result = check_is_admin(Success(User(..)))  # Result[User, Exception]
        """

        @wraps(func)
        def _if_ok(cnt: "Result[TOk, TBad]") -> "Result[TOk, TBad]":
            return cnt >> func

        return _if_ok

    @staticmethod
    def if_bad(
        func: Callable[[TBad], "Result[VOk, VBad]"],
    ) -> Callable[["Result[TOk, TBad]"], "Result[VOk, VBad]"]:
        """Decorator for functions that will be executed only with `Failure` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.if_bad
            def handle_error(err: Exception) -> str:
                ...

            result = handle_error(Failure(Exception(..)))  # Success[str]
        """

        @wraps(func)
        def _if_bad(cnt: "Result[TOk, TBad]") -> "Result[TOk, TBad]":
            return cnt << func

        return _if_bad

    @staticmethod
    def returns(
        func: Callable[[TOk], VOk | Exception]
    ) -> Callable[[TOk], Result[VOk, Exception]]:
        """When function returns `Exception` it is wrapped into `Bad`.

        Example::

                @Result.returns
                def divide_two_by(x: int) -> int | Exception:
                    match x:
                        case 0:
                            return ValueError('Cannot divide by zero')
                        case value:
                            return 2 / value

                divide_two_by(0)  # Failure(value=ValueError('Cannot divide by zero'))
        """

        @wraps(func)
        def _wrapper(value: TOk):
            match func(value):
                case Exception() as error:
                    return Bad(error)
                case value:
                    return Ok(value)

        return _wrapper

    @staticmethod
    def excepts(func: Callable[[TOk], VOk]) -> Callable[[TOk], Result[VOk, Exception]]:
        """When function raises `Exception` it is excepted and wrapped into `Bad`.

        Example::
                @Result.excepts
                def divide_one_by(x: int) -> int:
                    return 1 / x

                divide_one_by(0)  # Failure(value=ZeroDivisionError('division by zero'))
        """

        @wraps(func)
        def _wrapper(value: TOk) -> Result[VOk, Exception]:
            try:
                return Ok(func(value))
            except Exception as err:
                return Bad(err)

        return _wrapper

    @staticmethod
    def if_ok_returns(
        func: Callable[[TOk], VOk | Exception]
    ) -> Callable[[Result[TOk, TBad]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_ok` and `returns`."""
        return Result.if_ok(Result.returns(func))

    @staticmethod
    def if_bad_returns(
        func: Callable[[TOk], VOk | Exception]
    ) -> Callable[[Result[TOk, TBad]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_bad` and `returns`."""
        return Result.if_bad(Result.returns(func))

    @staticmethod
    def if_ok_excepts(
        func: Callable[[TOk], VOk]
    ) -> Callable[[Result[TOk, TBad]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_ok` and `excepts`."""
        return Result.if_ok(Result.excepts(func))

    @staticmethod
    def if_bad_excepts(
        func: Callable[[TOk], VOk]
    ) -> Callable[[Result[TOk, TBad]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_bad` and `excepts`."""
        return Result.if_bad(Result.excepts(func))

    def unpack(self) -> TOk | TBad:
        """Returns internal container value processed by `Result` monad."""
        return self.value


@dataclass(frozen=True, slots=True)
class Ok(Result[TOk, Any]):
    """Container that marks underlying value is `Ok` and can be processed next."""

    value: TOk


@dataclass(frozen=True, slots=True)
class Bad(Result[Any, TBad]):
    """Container that marks underlying value is `Bad` and connot be processed next."""

    value: TBad
