from dataclasses import dataclass
from functools import reduce, wraps
from inspect import isawaitable
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
                >> (lambda x: x + 1)
                >> async_inc
                >> async_power_2
            )  # Future (awaitable)
            print(await f)  # 25
    """

    value: Awaitable[T]

    def __await__(self) -> Generator[None, None, T]:
        return self.value.__await__()

    async def __bind(self, function: Callable[[T], Awaitable[V] | V]) -> V:
        result = function(await self.value)
        return await result if isawaitable(result) else result

    def __rshift__(self, func: Callable[[T], Awaitable[V] | V]) -> "Future[V]":
        return Future(self.__bind(func))

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
    def create(value: T) -> "Future[T]":
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

    @staticmethod
    def bound(
        func: Callable[[T], Awaitable[V] | V],
    ) -> Callable[["Future[T]"], "Future[V]"]:
        """Decorator for functions to make them work with `Futures`.

        Makes function automatically bindable for `Future` without `>>` syntax.

        Example::

                @Future.bound
                def plus_1(x: int) -> int:
                    return x + 1

                plus_1(Future.create(3))  # Future(4)
        """

        @wraps(func)
        def _bound(cnt: "Future[T]") -> "Future[V]":
            return cnt >> func

        return _bound

    @staticmethod
    def compose(*funcs: Callable[[T], Awaitable[V] | V]) -> Callable[[T], Awaitable[V]]:
        """Combinator for sync and async functions that converts them into async pipeline.

        If `funcs` is empty than returns async identity function.

        Example::

                composition = Future.compose(
                    async_plus_1,
                    sync_plus_1,
                )  # asynchronous function that executes async_func, than sync_func

                result = await (Future.create(3) >> composition)  # 5

        Returns:
            Callable[[T], Awaitable[V]]: function composition
        """
        match funcs:
            case ():
                return Future.identity
            case _:

                async def _composition(cnt: T) -> V:
                    return await reduce(lambda c, f: c >> f, funcs, Future.create(cnt))

                return _composition

    @staticmethod
    def do(
        cnt: T | "Future[T]", *funcs: Callable[[T], Awaitable[V] | V]
    ) -> "Future[V]":
        """Execute multiple sync and async function on some `Future` container.

        Basically this is for running some pipeline on some value. Supports both sync
        and `Future` values. Sequentially executes functions one-by-one via composition.
        Useful for cases when `funcs` are not known and come as first-class citizens and
        must be executed. In case functions to run are know use `>>` syntax for more
        readable pipeline execution syntax.

        Example::

                f = Future.do(
                    3,
                    lambda x: x + 1,
                    async_inc,
                    async_power_2
                )  # Future (awaitable)
                print(await f)  # 25

        Args:
            cnt (T | Future[T]): to use as argument for functions.

        Returns:
            Future[V]: result.
        """
        match cnt:
            case Future():
                return cnt >> Future.compose(*funcs)
            case _:
                return Future.create(cnt) >> Future.compose(*funcs)
