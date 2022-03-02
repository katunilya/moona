import inspect
from functools import reduce, wraps
from typing import Awaitable, TypeVar, Union

from typing_extensions import TypeAlias

from mona.types import Transform

T = TypeVar("T")
V = TypeVar("V")

_Awaitable: TypeAlias = Union[T, Awaitable[T]]


async def pack(value: _Awaitable[T]) -> T:
    """Wraps passed value into Awaitable if one is not already."""
    return await value if inspect.isawaitable(value) else value


async def bind(function: Transform[T, Awaitable[V]], monad: _Awaitable[T]) -> V:
    """Executes function waiting for passed Awaitable monad."""
    return await pack(function(await pack(monad)))


def compose(
    *functions: Transform[T, _Awaitable[V]]
) -> Transform[_Awaitable[T], Awaitable[V]]:
    """Composes multiple sync and async functions to work with Future values."""

    def _compose(monad: _Awaitable[T]) -> Awaitable[V]:
        return reduce(lambda m, f: bind(f, m), functions, monad)

    return _compose


def wrap(
    function: Transform[T, _Awaitable[V]]
) -> Transform[_Awaitable[T], Awaitable[V]]:
    """Decorated function now operates with Awaitable input values."""

    @wraps(function)
    def _wrapper(monad: _Awaitable[T]) -> Awaitable[V]:
        return bind(function, monad)

    return _wrapper
