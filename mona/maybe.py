import abc
import dataclasses
from typing import Any, Callable, TypeVar

import toolz

from mona import state

T = TypeVar("T")
V = TypeVar("V")


@dataclasses.dataclass(frozen=True)
class Maybe(state.State[T], abc.ABC):
    """General purpose container for optional value.

    `Maybe` container has 2 variations: `Some` and `Nothing`. `Some` stands for some
    actual value and means that it is present in execution context. `Nothing` on the
    other hand describes emtpiness and lack of value. This is additional wrapping around
    `None` values.

    Strict types help ignore
    """

    def __rshift__(self, func: Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        """Dunder method for `>>` bind syntax.

        >>> maybe.bind(function, cnt)
        >>> # exactly the same as
        >>> cnt >> function

        Args:
            func (Callable[[T], &quot;Maybe[V]&quot;]): _description_

        Returns:
            Maybe[V]: _description_
        """
        return bind(func, self)


@dataclasses.dataclass(frozen=True)
class Some(Maybe[T]):
    """Container for actually present value."""


@dataclasses.dataclass(frozen=True)
class Nothing(Maybe[Any]):
    """Private container for non-existent value."""

    __slots__ = ()
    __instance: "Nothing | None" = None

    def __new__(cls, *args, **kwargs) -> "Nothing":  # noqa
        match cls.__instance:
            case None:
                cls.__instance = object.__new__(cls)
                return cls.__instance
            case _:
                return cls.__instance

    def __init__(self) -> None:  # noqa
        super().__init__(None)


MaybeFunc = Callable[[T], Maybe[V]]


@toolz.curry
def bind(func: MaybeFunc[T, V], cnt: Maybe[T]) -> Maybe[V]:
    """Bind function for `Maybe` monad.

    `function` is executed only in case `cnt` is `Some` and not `Nothing` as it does not
    make any sense to execute some `function` with `Nothing`.

    Args:
        function (Callable[[Maybe[T]], Maybe[V]]): to bind
        cnt (Maybe[T]): `Maybe` container

    Returns:
        Maybe[V]: result of running `function` on `cnt` value.
    """
    match cnt:
        case Some(value):
            return func(value)
        case _:
            return cnt


def or_value(value: T) -> MaybeFunc[V, T | V]:
    """Recovers from `Nothing` or just passes `Some`.

    When `Some` value is passed nothing is done and it is just returned. When `Nothing`
    is passed than it is repaced with `Some` `value`.

    Args:
        value (T): to recover to

    Returns:
        Callable[[Maybe[V]], Maybe[V] | Maybe[T]]: maybe handler function
    """

    def _or_value(cnt: Maybe[V]) -> Maybe[V] | Maybe[T]:
        match cnt:
            case Some():
                return cnt
            case _:
                return Some(value)

    return _or_value


def _continue_on_some(cur: MaybeFunc[T, V], nxt: MaybeFunc[T, V]) -> MaybeFunc[T, V]:
    def __continue_on_some(val: T):
        match cur(val):
            case Some(result):
                return result
            case Nothing():
                return nxt(val)

    return __continue_on_some


def choose(*functions: MaybeFunc[T, V]) -> MaybeFunc[T, V]:
    """Return first `Some` result from passed functions.

    If `functions` is empty, than return `Nothing`.
    If no `function` can return `Some` than return `Nothing`.
    """

    def _choose(value: T):
        match functions:
            case ():
                return Nothing()
            case _:
                return toolz.reduce(_continue_on_some, functions)(value)

    return _choose
