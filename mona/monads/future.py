from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Awaitable, Callable, Generator, Generic, TypeVar

from mona.monads.core import Bindable
from mona.monads.maybe import FutureMaybe, Maybe
from mona.monads.result import FutureResult, Result, TError, TOk

T = TypeVar("T")
V = TypeVar("V")


@dataclass(frozen=True)
class Future(Bindable, Generic[T]):
    """Container for performing asynchronous operations on some value in sync context.

    `Future` allows running async function inside synchronous functions. Can execute
    both sync and async functions and produce next `Future`s.

    Example::

            f = (
                Future.create(3)
                .then(lambda x: x + 1)
                .then_future(async_inc)
                .then_future(async_power_2)
            )  # Future (awaitable)
            print(await f)  # 25
    """

    value: Awaitable[T]

    def __await__(self) -> Generator[None, None, T]:
        return self.value.__await__()

    async def __then_future(self, func: Callable[[T], Awaitable[V]]) -> V:
        return await func(await self.value)

    async def __then(self, func: Callable[[T], V]) -> V:
        return func(await self.value)

    def then(self, func: Callable[[T], V]) -> Future[V]:
        """Execute sync `func` on `Future` value and return `Future`.

        Args:
            func (Callable[[T], V]): to execute.

        Returns:
            Future[V]: execution result.
        """
        return Future(self.__then(func))

    def then_result(
        self, func: Callable[[T], Result[TOk, TError]]
    ) -> FutureResult[TOk, TError]:
        """Execute sync `func` on `Future` value and return `FutureResult`.

        Args:
            func (Callable[[T], Result[TOk, TBad]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__then(func))

    def then_maybe(self, func: Callable[[T], Maybe[V]]) -> FutureMaybe[V]:
        """Execute sync `func` on `Future` value and return `FutureMaybe`.

        Args:
            func (Callable[[T], Maybe[V]]): to execute.

        Returns:
            FutureMaybe[V]: result.
        """
        return FutureMaybe(self.__then(func))

    def then_future(self, func: Callable[[T], Awaitable[V]]) -> Future[V]:
        """Execute async `func` on `Future` value and return `Future`.

        Args:
            func (Callable[[T], Awaitable[V]]): to execute.

        Returns:
            Future[V]: execution result.
        """
        return Future(self.__then_future(func))

    def then_future_result(
        self, func: Callable[[T], Awaitable[Result[TOk, TError]]]
    ) -> FutureResult[TOk, TError]:
        """Execute async `func` on `Future` value and return `FutureResult`.

        Args:
            func (Callable[[T], Awaitable[Result[TOk, TBad]]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: result.
        """
        return FutureResult(self.__then_future(func))

    def then_future_maybe(
        self, func: Callable[[T], Awaitable[Maybe[V]]]
    ) -> FutureMaybe[V]:
        """Execute async `func` on `Future` value and return `FutureMaybe`.

        Args:
            func (Callable[[T], Awaitable[Maybe[V]]]): to execute.

        Returns:
            FutureMaybe[V]: result.
        """
        return FutureResult(self.__then_future(func))

    @staticmethod
    async def identity(value: T) -> T:
        """Asynchronously returns passed `value`.

        Example::

                f = Future.identity(3)  # awaitable 3
                print(await f)  # 3

        Args:
            value (T): to return asynchronously

        Returns:
            T: return value
        """
        return value

    @staticmethod
    def from_value(value: T) -> Future[T]:
        """Create future from some present value (not awaitable).

        Example::

                f = Future.from_value(1)
                print(await f)  # 1

        Args:
            value (T): value to wrap into `Future`

        Returns:
            Future[T]: result
        """
        return Future(Future.identity(value))

    @staticmethod
    def returns(func: Callable[[T], Awaitable[V]]) -> Callable[[T], Future[V]]:
        """Decorator for wrapping awaitable value returned from `func` to `Future`."""

        @wraps(func)
        def _wrapper(value: T) -> Future[V]:
            return Future(func(value))

        return _wrapper
