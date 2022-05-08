from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Generator, Generic, TypeVar

from mona.monads.core import Bindable

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
                > (lambda x: x + 1)
                >> async_inc
                >> async_power_2
            )  # Future (awaitable)
            print(await f)  # 25
    """

    value: Awaitable[T]

    def __await__(self) -> Generator[None, None, T]:
        return self.value.__await__()

    async def __bind_async(self, func: Callable[[T], Awaitable[V]]) -> V:
        return await func(await self.value)

    async def __bind_sync(self, func: Callable[[T], V]) -> V:
        return func(await self.value)

    def __rshift__(self, func: Callable[[T], Awaitable[V]]) -> Future[V]:
        return Future(self.__bind_async(func))

    def __gt__(self, func: Callable[[T], V]) -> Future[V]:
        return Future(self.__bind_sync(func))

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
    def create(value: T) -> Future[T]:
        """Create future from some present value (not awaitable).

        Example::

                f = Future.create(1)
                print(await f)  # 1

        Args:
            value (T): value to wrap into `Future`

        Returns:
            Future[T]: result
        """
        return Future(Future.identity(value))
