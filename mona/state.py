from dataclasses import dataclass
from functools import reduce, wraps
from typing import Generic, TypeVar, Union

from mona.types import Transform

T = TypeVar("T")
V = TypeVar("V")


@dataclass(frozen=True)
class State(Generic[T]):
    """Immutable container for adding state of wrapped value.

    Attributes:
        value (T): wrapped value stored in container
        valid (bool): marker for state of the container. True - valid, False - invalid
    """

    __slots__ = ("value", "valid")

    value: T
    valid: bool


_State = Union[T, State[T]]


def valid(value: _State[T]) -> State[T]:
    """Packs value into valid State container."""
    if isinstance(value, State):
        return State(value.value, True)
    return State(value, True)


def invalid(value: _State[T]) -> State[T]:
    """Packs value into invalid State container."""
    if isinstance(value, State):
        return State(value.value, False)
    return State(value, False)


def pack(value: _State[T]) -> State[T]:
    """Wraps value into Valid container if value is not container itself."""
    if isinstance(value, State):
        return value

    return valid(value)


def unpack(monad: _State[T]) -> T:
    """Extracts value from container or just returns value if one is not monad."""
    if isinstance(monad, State):
        return monad.value
    return monad


def bind(function: Transform[_State[T], _State[V]], monad: _State[T]) -> State[V]:
    """Execute function only when monad is not in invalid State."""
    if isinstance(monad, State) and monad.valid is False:
        return monad

    return pack(function(unpack(monad)))


def wrap(function: Transform[_State[T], _State[V]]) -> Transform[_State[T], State[V]]:
    """Passed function is executed based on State monad rules."""

    @wraps(function)
    def _wrapper(monad: _State[T]) -> State[V]:
        return bind(function, monad)

    return _wrapper


def compose(
    *functions: Transform[_State[T], State[V]]
) -> Transform[_State[T], State[T]]:
    """Composes multiple monadic functions into one sequential execution of them."""

    @wrap
    def _compose(monad: _State[T]) -> State[V]:
        return reduce(lambda m, f: bind(f, m), functions, monad)

    return _compose


def choose(
    *functions: Transform[_State[T], _State[V]]
) -> Transform[_State[T], State[V]]:
    """Compose multiple functions where result of execution is the first Valid state."""

    @wrap
    def _choose(monad: _State[T]) -> State[V]:
        return next(
            (
                result
                for result in (bind(func, monad) for func in functions)
                if result.valid
            ),
            monad,
        )

    return _choose
