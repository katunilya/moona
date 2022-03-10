from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
V = TypeVar("V")


@dataclass(frozen=True)
class Valid(Generic[T]):
    """Container for `Valid` `State` of `value`."""

    __slots__ = "value"

    value: T


@dataclass(frozen=True)
class Invalid(Generic[T]):
    """Container for `Invalid` `State` of `value`."""

    __slots__ = "value"

    value: T


State = Union[Valid[T], Invalid[T]]
_State = Union[T, State[T]]


def is_state(value: _State[T]) -> bool:
    """`True` if `value` is `Valid` or `Invalid`."""
    return isinstance(value, (Valid, Invalid))


def is_valid(value: _State[T]) -> bool:
    """`True` if `value` is `Valid`."""
    return isinstance(value, Valid)


def is_invalid(value: _State[T]) -> bool:
    """`True` if `value` is `Invalid`."""
    return isinstance(value, Invalid)


def valid(value: _State[T]) -> Valid[T]:
    """Packs passed `value` into `Valid` container, even if it is `Invalid`."""
    return Valid(value.value if isinstance(value, (Valid, Invalid)) else value)


def invalid(value: _State[T]) -> Invalid[T]:
    """Packs passed `value` into `Invalid` container, even if it is `Valid`."""
    return Invalid(value.value if isinstance(value, (Valid, Invalid)) else value)


def pack(value: _State[T]) -> State[T]:
    """Packs `value` into `Valid` container if one is not container already."""
    return value if isinstance(value, (Valid, Invalid)) else Valid(value)


def unpack(monad: _State[T]) -> T:
    """Returns `value` of `monad` if one is `State`, else returns `monad` itself."""
    return monad.value if isinstance(monad, (Valid, Invalid)) else monad


def bind(function: Callable[[T], _State[V]], monad: _State[T]) -> State[V]:
    """Executes `function` only if `monad` is not in `INvalid"""
    if isinstance(monad, Invalid):
        return monad

    return pack(function(unpack(monad)))


def compose(*functions: Callable[[T], _State[V]]) -> Callable[[_State[T]], State[V]]:
    """Composition of multiple `functions` with `State` monad binding."""

    def _compose(monad: _State[T]) -> State[V]:
        monad = pack(monad)

        if isinstance(monad, Invalid):
            return monad

        return reduce(lambda m, f: bind(f, m), functions, monad)

    return _compose


def choose(*functions: Callable[[T], _State[V]]) -> Callable[[_State[T]], State[V]]:
    """Composition that returns first `Valid` result of `functions` execution."""

    def _choose(monad: _State[T]) -> State[V]:
        monad = pack(monad)

        if isinstance(monad, Invalid):
            return monad

        return next(
            (
                monad_
                for monad_ in (bind(func, monad) for func in functions)
                if isinstance(monad_, Valid)
            ),
            monad,
        )

    return _choose
