import inspect
from functools import reduce
from typing import Awaitable, Callable, TypeVar, Union

from typing_extensions import TypeAlias

T = TypeVar("T")
V = TypeVar("V")

_Awaitable: TypeAlias = Union[T, Awaitable[T]]


async def pack_value(value: T) -> T:
    """Simple async identity functions that pack `value` into `Awaitable`."""
    return value


async def pack(value: _Awaitable[T]) -> T:
    """Wraps passed value into Awaitable if one is not already."""
    return await value if inspect.isawaitable(value) else value


async def bind(function: Callable[[T], _Awaitable[V]], monad: _Awaitable[T]) -> V:
    """Executes function waiting for passed Awaitable monad."""
    if inspect.isawaitable(monad):
        monad = await monad

    return await pack(function(monad))


def compose(
    *functions: Callable[[T], _Awaitable[V]]
) -> Callable[[_Awaitable[T]], Awaitable[V]]:
    """Composes multiple sync and async functions to work with Future values."""

    def _compose(monad: _Awaitable[T]) -> Awaitable[V]:
        return reduce(lambda m, f: bind(f, m), functions, monad)

    return _compose
