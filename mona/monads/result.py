from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Any, Awaitable, Callable, Generator, Generic, TypeVar

TOk = TypeVar("TOk")
TError = TypeVar("TError")
VOk = TypeVar("VOk")
VError = TypeVar("VError")


@dataclass(frozen=True, slots=True)
class FutureResult(Generic[TOk, TError], ABC):
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

    value: Awaitable[Result[TOk, TError]]

    def __await__(self) -> Generator[None, None, Result[TOk, TError]]:
        return self.value.__await__()

    async def __then(
        self, func: Callable[[TOk], Result[VOk, VError]]
    ) -> Result[TOk, TError]:
        match await self.value:
            case Ok(value):
                return func(value)
            case Error() as bad:
                return bad

    def then(
        self, func: Callable[[TOk], Result[VOk, VError]]
    ) -> FutureResult[TOk, TError]:
        """Execute sync `func` if async result is `Ok`.

        Args:
            func (Callable[[TOk], Result[VOk, VError]]): to execute.

        Returns:
            FutureResult[TOk, TError]: result.
        """
        return FutureResult(self.__then(func))

    async def __otherwise(
        self, func: Callable[[TError], Result[VOk, VError]]
    ) -> Result[VOk, VError]:
        match await self.value:
            case Error(value):
                return func(value)
            case Ok() as ok:
                return ok

    def otherwise(
        self, func: Callable[[TError], Result[VOk, VError]]
    ) -> FutureResult[TOk, TError]:
        """Execute sync `func` if async result is `Bad`.

        Args:
            func (Callable[[TError], Result[VOk, VError]]): to execute.

        Returns:
            FutureResult[TOk, TError]: result.
        """
        return FutureResult(self.__otherwise(func))

    async def __then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VError]]]
    ) -> Result[TOk, TError]:
        match await self.value:
            case Ok(value):
                return await func(value)
            case Error() as bad:
                return bad

    def then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VError]]]
    ) -> FutureResult[TOk, TError]:
        """Execute async `func` if async result is `Ok`.

        Args:
            func (Callable[[TOk], Awaitable[Result[VOk, VError]]]): to execute.

        Returns:
            FutureResult[TOk, TError]: result.
        """
        return FutureResult(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[TError], Awaitable[Result[VOk, VError]]]
    ) -> Result[TOk, TError]:
        match await self.value:
            case Error(value):
                return await func(value)
            case Ok() as ok:
                return ok

    def otherwise_future(
        self, func: Callable[[TError], Awaitable[Result[VOk, VError]]]
    ) -> FutureResult[TOk, TError]:
        """Execute async `func` if async result if `Bad`..

        Args:
            func (Callable[[TError], Awaitable[Result[VOk, VError]]]): to execute.

        Returns:
            FutureResult[TOk, TError]: result.
        """
        return FutureResult(self.__otherwise_future(func))

    @staticmethod
    def if_ok(
        func: Callable[[TOk], Awaitable[Result[VOk, VError]]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, VError]]]:
        """Decorator that executes async `func` only if `Ok` is passed."""

        @wraps(func)
        async def _wrapper(cnt: Result[TOk, TError]) -> Result[VOk, VError]:
            match cnt:
                case Ok(value):
                    return await func(value)
                case Error() as err:
                    return err

        return _wrapper

    @staticmethod
    def if_error(
        func: Callable[[TError], Awaitable[Result[VOk, VError]]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, VError]]]:
        """Decorator that executes async `func` only if `Error` is passed."""

        @wraps(func)
        async def _wrapper(cnt: Result[TOk, TError]) -> Result[VOk, VError]:
            match cnt:
                case Ok() as ok:
                    return ok
                case Error(value):
                    return await func(value)

        return _wrapper

    @staticmethod
    def returns(
        func: Callable[[TOk], Awaitable[VOk | Exception]]
    ) -> Callable[[TOk], Awaitable[Result[VOk, Exception]]]:
        """Decorator that wraps async result of `func` into `Result`.

        If `Exception` is returned, than it is wrapped into `Error`. If something else
        is returned that it is wrapped into `Ok`.
        """

        @wraps(func)
        async def _wrapper(arg: TOk) -> Result[VOk, VError]:
            match await func(arg):
                case Exception() as exc:
                    return Error(exc)
                case value:
                    return Ok(value)

        return _wrapper

    @staticmethod
    def excepts(
        func: Callable[[TOk], Awaitable[VOk]]
    ) -> Callable[[TOk], Awaitable[Result[VOk, Exception]]]:
        """Decorator that excepts `Exception` to be raised from async `func`.

        If `Exception` is raised that it is excepted and wrapped into `Error`. Otherwise
        result is wrapped into `Ok`.
        """

        @wraps(func)
        async def _wrapper(arg: TOk) -> Result[VOk, VError]:
            try:
                return Ok(await func(arg))
            except Exception() as exc:
                return Error(exc)

        return _wrapper

    @staticmethod
    def if_ok_returns(
        func: Callable[[TOk], Awaitable[VOk | Exception]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, Exception]]]:
        """Decorator that combines `if_ok` and `returns`."""

        @wraps(func)
        async def _wrapper(arg: Result[TOk, TError]) -> Result[VOk, VError]:
            match arg:
                case Ok(value):
                    match await func(value):
                        case Exception() as exc:
                            return Error(exc)
                        case result:
                            return Ok(result)
                case Error() as err:
                    return err

        return _wrapper

    @staticmethod
    def if_error_returns(
        func: Callable[[TError], Awaitable[VOk | Exception]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, Exception]]]:
        """Decorator that combines `if_error` and `returns`."""

        @wraps(func)
        async def _wrapper(arg: Result[TOk, TError]) -> Result[VOk, VError]:
            match arg:
                case Error(value):
                    match await func(value):
                        case Exception() as exc:
                            return Error(exc)
                        case result:
                            return Ok(result)
                case Ok() as ok:
                    return ok

        return _wrapper

    @staticmethod
    def if_ok_excepts(
        func: Callable[[TOk], Awaitable[VOk]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, Exception]]]:
        """Decorator that combines `if_ok` and `excepts`."""

        @wraps(func)
        async def _wrapper(arg: Result[TOk, TError]) -> Result[VOk, VError]:
            match arg:
                case Ok(value):
                    try:
                        return Ok(await func(value))
                    except Exception as exc:
                        return Error(exc)
                case Error() as err:
                    return err

        return _wrapper

    @staticmethod
    def if_error_excepts(
        func: Callable[[TError], Awaitable[VOk]]
    ) -> Callable[[Result[TOk, TError]], Awaitable[Result[VOk, Exception]]]:
        """Decorator that combines `if_error` and `excepts`."""

        @wraps(func)
        async def _wrapper(arg: Result[TOk, TError]) -> Result[VOk, VError]:
            match arg:
                case Error(value):
                    try:
                        return Ok(await func(value))
                    except Exception as exc:
                        return Error(exc)
                case Ok() as ok:
                    return ok

        return _wrapper


@dataclass(frozen=True, slots=True)
class Result(Generic[TOk, TError], ABC):
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

    value: TOk | TError

    def then(self, func: Callable[[TOk], Result[VOk, VError]]) -> Result[VOk, VError]:
        """Binding for sync function that handle `Ok`.

        Executes passed function only when container is `Ok`, otherwise just returns
        container.

        Args:
            func (Callable[[TOk], Result[VOk, VError]]): to execute.

        Returns:
            Result[VOk, VError]: result of function execution or initial monad container
            if one was `Bad`.
        """
        match self:
            case Ok(value):
                return func(value)
            case Error() as bad:
                return bad

    def otherwise(
        self, func: Callable[[TError], Result[VOk, VError]]
    ) -> Result[VOk, VError]:
        """Binding for sync function that handle `Bad`.

        Executes passed function only when container is `Bad`, otherwise just returns
        container.

        Args:
            func (Callable[[TError], Result[VOk, VError]]): to execute.

        Returns:
            Result[VOk, VError]: result if function execution or initial monad container
            if one is `Ok`.
        """
        match self:
            case Error(value):
                return func(value)
            case Ok() as ok:
                return ok

    async def __then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VError]]]
    ) -> Result[VOk, VError]:
        match self:
            case Ok(value):
                return await func(value)
            case Error() as bad:
                return bad

    def then_future(
        self, func: Callable[[TOk], Awaitable[Result[VOk, VError]]]
    ) -> FutureResult[VOk, VError]:
        """Execute async `func` if `Result` value is `Ok` and return `FutureResult`.

        Args:
            func (Callable[[TOk], Awaitable[Result[VOk, VError]]]): to execute.

        Returns:
            FutureResult[VOk, VError]: result.
        """
        return FutureResult(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[TError], Awaitable[Result[VOk, VError]]]
    ) -> Result[VOk, VError]:
        match self:
            case Error(value):
                return await func(value)
            case Ok() as ok:
                return ok

    def otherwise_future(
        self, func: Callable[[TError], Awaitable[Result[VOk, VError]]]
    ) -> FutureResult[VOk, VError]:
        """Execute async `func` if `Result` value is `Error` and return `FutureResult`.

        Args:
            func (Callable[[TError], Awaitable[Result[VOk, VError]]]): to execute.

        Returns:
            FutureResult[VOk, VError]: result.
        """
        return FutureResult(self.__otherwise_future(func))

    @staticmethod
    def if_ok(
        func: Callable[[TOk], "Result[VOk, VError]"],
    ) -> Callable[["Result[TOk, TError]"], "Result[VOk, VError]"]:
        """Decorator for functions that will be executed only with `Success` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.if_ok
            def check_is_admin(user: User) -> User:
                ...

            result = check_is_admin(Success(User(..)))  # Result[User, Exception]
        """

        @wraps(func)
        def _if_ok(cnt: "Result[TOk, TError]") -> "Result[TOk, TError]":
            return cnt >> func

        return _if_ok

    @staticmethod
    def if_error(
        func: Callable[[TError], "Result[VOk, VError]"],
    ) -> Callable[["Result[TOk, TError]"], "Result[VOk, VError]"]:
        """Decorator for functions that will be executed only with `Failure` `Result`.

        Changes input and output types for passed function to `Result`.

        Example::

            @Result.if_error
            def handle_error(err: Exception) -> str:
                ...

            result = handle_error(Failure(Exception(..)))  # Success[str]
        """

        @wraps(func)
        def _if_bad(cnt: "Result[TOk, TError]") -> "Result[TOk, TError]":
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
                    return Error(error)
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
                return Error(err)

        return _wrapper

    @staticmethod
    def if_ok_returns(
        func: Callable[[TOk], VOk | Exception]
    ) -> Callable[[Result[TOk, TError]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_ok` and `returns`."""
        return Result.if_ok(Result.returns(func))

    @staticmethod
    def if_error_returns(
        func: Callable[[TOk], VOk | Exception]
    ) -> Callable[[Result[TOk, TError]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_bad` and `returns`."""
        return Result.if_error(Result.returns(func))

    @staticmethod
    def if_ok_excepts(
        func: Callable[[TOk], VOk]
    ) -> Callable[[Result[TOk, TError]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_ok` and `excepts`."""
        return Result.if_ok(Result.excepts(func))

    @staticmethod
    def if_error_excepts(
        func: Callable[[TOk], VOk]
    ) -> Callable[[Result[TOk, TError]], Result[VOk, Exception]]:
        """Decorator for functions that combines `if_bad` and `excepts`."""
        return Result.if_error(Result.excepts(func))

    def unpack(self) -> TOk | TError:
        """Returns internal container value processed by `Result` monad."""
        return self.value


@dataclass(frozen=True, slots=True)
class Ok(Result[TOk, Any]):
    """Container that marks underlying value is `Ok` and can be processed next."""

    value: TOk


@dataclass(frozen=True, slots=True)
class Error(Result[Any, TError]):
    """Container that marks underlying value is `Bad` and connot be processed next."""

    value: TError
