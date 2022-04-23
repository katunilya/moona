import abc
import dataclasses
import typing

import toolz

from mona import state

T = typing.TypeVar("T")
V = typing.TypeVar("V")


@dataclasses.dataclass(frozen=True)
class Maybe(state.State[T], abc.ABC):
    """General purpose container for optional value.

    `Maybe` container has 2 variations: `Some` and `Nothing`. `Some` stands for some
    actual value and means that it is present in execution context. `Nothing` on the
    other hand describes emtpiness and lack of value. This is additional wrapping around
    `None` values.

    Strict types help ignore
    """

    def __rshift__(self, func: typing.Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        """Dunder method for `>>` bind syntax.

        >>> maybe.bind(function, cnt)
        >>> # exactly the same as
        >>> cnt >> function

        Args:
            func (typing.Callable[[T], &quot;Maybe[V]&quot;]): _description_

        Returns:
            Maybe[V]: _description_
        """
        return bind(func, self)


@dataclasses.dataclass(frozen=True)
class Some(Maybe[T]):
    """Container for actually present value."""


@dataclasses.dataclass(frozen=True)
class _Nothing(Maybe[typing.Any]):
    """Private container for non-existent value."""

    __slots__ = ()
    __instance: "_Nothing | None" = None

    def __new__(cls, *args, **kwargs) -> "_Nothing":
        match cls.__instance:
            case None:
                cls.__instance = object.__new__(cls)
                return cls.__instance
            case _:
                return cls.__instance

    def __init__(self) -> None:
        super().__init__(None)


Nothing = _Nothing()


@toolz.curry
def bind(func: typing.Callable[[T], Maybe[V]], cnt: Maybe[T]) -> Maybe[V]:
    """Bind function for `Maybe` monad.

    `function` is executed only in case `cnt` is `Some` and not `Nothing` as it does not
    make any sense to execute some `function` with `Nothing`.

    Args:
        function (typing.Callable[[Maybe[T]], Maybe[V]]): to bind
        cnt (Maybe[T]): `Maybe` container

    Returns:
        Maybe[V]: result of running `function` on `cnt` value.
    """
    match cnt:
        case Some(value):
            return func(value)
        case _:
            return cnt
