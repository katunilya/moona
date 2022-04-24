import abc
import dataclasses
import functools
from typing import Any, Callable, Generic, TypeVar

from mona.monads.core import Alterable, Bindable

TSome = TypeVar("TSome")
VSome = TypeVar("VSome")


@dataclasses.dataclass(frozen=True)
class Maybe(Bindable, Alterable, Generic[TSome], abc.ABC):
    """General purpose container for optional value.

    `Maybe` container has 2 variations: `Some` and `Nothing`. `Some` stands for some
    actual value and means that it is present in execution context. `Nothing` on the
    other hand describes emtpiness and lack of value. This is additional wrapping around
    `None` values.
    """

    value: TSome

    def __rshift__(self, func: Callable[[TSome], "Maybe[VSome]"]) -> "Maybe[VSome]":
        """Dunder method for `>>` bind syntax.

        Perform execution of `func` only when container is `Some`. In case container is
        `Nothing` just return it.

        Args:
            func (Callable[[T], Maybe[V]]): to bind

        Returns:
            Maybe[V]: result
        """
        match self:
            case Some(value):
                return func(value)
            case Nothing() as nothing:
                return nothing

    def __lshift__(self, func: Callable[["Nothing"], "Maybe[TSome]"]) -> "Maybe[TSome]":
        """Dunder method for `<<` altering.

        Perform execution of `func` only when container is `Nothing`. In case container
        is `Some` just return it.

        Args:
            func (Callable[[Nothing], Maybe[TSome]]): to alter

        Returns:
            Maybe[TSome]: result
        """
        match self:
            case Nothing() as nothing:
                return func(nothing)
            case Some() as some:
                return some


@dataclasses.dataclass(frozen=True)
class Some(Maybe[TSome]):
    """`Maybe` container for values that are actually present."""


@dataclasses.dataclass(frozen=True)
class Nothing(Maybe[Any]):
    """Singleton `Maybe` container marking value absence."""

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


MaybeFunc = Callable[[TSome], Maybe[VSome]]


def bind(func: MaybeFunc[TSome, VSome], cnt: Maybe[TSome]) -> Maybe[VSome]:
    """Bind function for `Maybe` monad.

    `function` is executed only in case `cnt` is `Some` and not `Nothing` as it does not
    make any sense to execute some `function` with `Nothing`.

    Args:
        function (Callable[[Maybe[T]], Maybe[V]]): to bind
        cnt (Maybe[T]): `Maybe` container

    Returns:
        Maybe[V]: result of running `function` on `cnt` value.
    """
    return cnt >> func


def alter(
    func: Callable[[Nothing], Maybe[VSome]], cnt: Maybe[TSome]
) -> Maybe[TSome | VSome]:
    """Alter function for `Maybe` monad.

    Args:
        func (Callable[[Nothing], Maybe[VSome]]): function to alter
        cnt (Maybe[TSome]): `Maybe` container

    Returns:
        Maybe[TSome | VSome]: result
    """
    return cnt << func


def or_value(value: TSome) -> MaybeFunc[VSome, TSome | VSome]:
    """Recovers from `Nothing` or just passes `Some`.

    When `Some` value is passed nothing is done and it is just returned. When `Nothing`
    is passed than it is repaced with `Some` `value`.

    Example::

            Nothing() << or_value(1) ##  Some(1)

    Args:
        value (T): to replace `Nothing` with

    Returns:
        Callable[[Maybe[V]], Maybe[V] | Maybe[T]]: maybe handler function
    """

    def _or_value(cnt: Maybe[VSome]) -> Maybe[VSome] | Maybe[TSome]:
        match cnt:
            case Some() as some:
                return some
            case Nothing():
                return Some(value)

    return _or_value


def _continue_on_some(
    cur: MaybeFunc[TSome, VSome], nxt: MaybeFunc[TSome, VSome]
) -> MaybeFunc[TSome, VSome]:
    def __continue_on_some(val: TSome):
        match cur(val):
            case Some(result):
                return result
            case Nothing():
                return nxt(val)

    return __continue_on_some


def choose(*functions: MaybeFunc[TSome, VSome]) -> MaybeFunc[TSome, VSome]:
    """Return first `Some` result from passed functions.

    If `functions` is empty, than return `Nothing`.
    If no `function` can return `Some` than return `Nothing`.

    Example::

            result = Some(1) >> choose(
                lambda x: Nothing(),
                lambda x: Some(2)
            )  # Some(2)
    """

    def _choose(value: TSome):
        match functions:
            case ():
                return Nothing()
            case _:
                return functools.reduce(_continue_on_some, functions)(value)

    return _choose


def no_none(func: Callable[[TSome], VSome | None]) -> Callable[[TSome], Maybe[VSome]]:
    """Decorator for functions that might return `None`.

    When decorated function returns `None` it is converted to `Nothing`, otherwise
    wrapped into `Some` container.

    Example::

            @no_none
            def func(x: int) -> int | None:
                return x if x > 10 else None

            Some(1) >> func  # Nothing
    """

    @functools.wraps(func)
    def _wrapper(value: TSome):
        match func(value):
            case None:
                return Nothing()
            case result:
                return Some(result)

    return _wrapper
