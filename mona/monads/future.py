import dataclasses
import functools
import inspect
from typing import Awaitable, Callable, Generator, Generic, TypeVar

from mona.monads.core import Bindable

T = TypeVar("T")
V = TypeVar("V")


@dataclasses.dataclass(frozen=True)
class Future(Bindable, Generic[T]):
    """Container for performing asynchronous operations on some value in sync context.

    `Future` allows running async function inside synchronous functions. Can execute
    both sync and async functions and produce next `Future`s.
    """

    value: Awaitable[T]

    def __await__(self) -> Generator[None, None, T]:
        """Dunder function that makes `Future` awaitable."""
        return self.value.__await__()

    async def __bind(self, function: Callable[[T], Awaitable[V] | V]) -> V:
        result = function(await self.value)
        return await result if inspect.isawaitable(result) else result

    def __rshift__(self, func: Callable[[T], V | Awaitable[V]]) -> "Future[V]":
        """Execute passed function synchronously even if it is async.

        Via bind operator we can execute sync or async `func` on this `Future` and get
        another `Future` as a result of computation.

        Examples::

                result = (Future.from_value(3)
                    >> lambda x: x + 1
                    >> async_plus_2
                )  # Awaitable

                print(await result)  # 5

        Args:
            func (Callable[[T], V  |  Awaitable[V]]): to execute

        Returns:
            Future[V]: result
        """
        return Future(self.__bind(func))


async def identity(value: T) -> T:
    """Asynchronously returns passed `value`.

    Args:
        value (T): to return asynchronously

    Returns:
        T: return value
    """
    return value


def from_value(value: T) -> "Future[T]":
    """Create future from some present value (not awaitable).

    Example::
            f = Future.from_value(1)
            print(await f)  # 1

    Args:
        value (T): value to wrap into `Future`

    Returns:
        Future[T]: result
    """
    return Future(identity(value))


def compose(*funcs: Callable[[T], Awaitable[V] | V]) -> Callable[[T], Awaitable[V]]:
    """Combinator for sync and async functions that converts them into async pipeline.

    If `funcs` is empty than returns async identity function.

    Example::

            composition = future.compose(
                async_plus_1,
                sync_plus_1,
            )  # asynchronous function that executes async_func, than sync_func

            result = await (Future.from_value(3) >> composition)  # 5

    Returns:
        Callable[[T], Awaitable[V]]: function composition
    """
    match funcs:
        case ():
            return identity
        case _:

            async def _composition(cnt: T) -> V:
                return await functools.reduce(
                    lambda c, f: c >> f, funcs, from_value(cnt)
                )

            return _composition
