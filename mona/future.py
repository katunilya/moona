import dataclasses
import inspect
import typing

import toolz

T = typing.TypeVar("T")
V = typing.TypeVar("V")


@dataclasses.dataclass(frozen=True)
class Future(typing.Generic[T]):
    """Container for awaitable values."""

    value: typing.Awaitable[T]

    def __await__(self) -> typing.Generator[None, None, T]:
        """Dunder function that makes `Future` awaitable."""
        return self.value.__await__()

    def __rshift__(
        self, function: typing.Callable[["Future[T]"], "Future[V]"]
    ) -> "Future[V]":
        """Dunder function for >> syntax of executing futures."""
        return bind(function, self)


async def identity(value: T) -> T:
    """Converts some value into Awaitable.

    Args:
        value (T): to be converted to awaitable.

    Returns:
        T: awaitable value
    """
    return value


def from_value(value: T) -> Future[T]:
    """Create `Future` from value.

    Do not pass here another `Awaitable`.

    Args:
        value (T): value to create awaitable.

    Returns:
        Future[T]: ready-to-use future
    """
    return Future(identity(value))


async def __bind(
    function: typing.Callable[[T], typing.Union[typing.Awaitable[V], V]], cnt: Future[T]
) -> V:
    result = function(await cnt)
    return await result if inspect.isawaitable(result) else result


@toolz.curry
def bind(
    function: typing.Callable[[T], typing.Union[typing.Awaitable[V], V]], cnt: Future[T]
) -> Future[V]:
    """Bind sync or async function to Future.

    Args:
        function (typing.Callable[[T], typing.Union[V, typing.Awaitable[V]]]): to bind
        cnt (Future[T]): container

    Returns:
        Future[V]: result of running `function` on `cnt` value
    """
    return Future(__bind(function, cnt))


def compose(
    *functions: typing.Callable[[T], typing.Union[V, typing.Awaitable[V]]]
) -> typing.Callable[[T], typing.Awaitable[V]]:
    """Converts sequence of functions into sequenced pipeline for `Future` container.

    Returns:
        typing.Callable[[Future[T]], Future[V]]: function composition
    """

    async def _composition(cnt: T) -> V:
        cnt = from_value(cnt)

        for func in functions:
            cnt = bind(func, cnt)

        return await cnt

    return _composition


def pipe(
    cnt: Future[T],
    *functions: typing.Union[
        typing.Callable[[T], typing.Awaitable[V]], typing.Callable[[T], V]
    ],
) -> Future[V]:
    """Composes `functions` and executes on `cnt`.

    Args:
        cnt (Future[T]): to execute

    Returns:
        Future[V]: result future
    """
    composition = compose(*functions)
    return cnt >> composition
