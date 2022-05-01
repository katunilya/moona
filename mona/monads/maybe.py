from abc import ABC
from dataclasses import dataclass
from functools import reduce, wraps
from typing import Any, Callable, Generic, TypeVar

from mona.monads.core import Alterable, Bindable

TSome = TypeVar("TSome")
VSome = TypeVar("VSome")


@dataclass(frozen=True)
class Maybe(Bindable, Alterable, Generic[TSome], ABC):
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
            func (Callable[[T], Maybe[V]]): to bind.

        Returns:
            Maybe[V]: result.
        """
        match self:
            case Some(value):
                return func(value)
            case Nothing() as nothing:
                return nothing

    def __lshift__(self, func: Callable[[None], "Maybe[VSome]"]) -> "Maybe[VSome]":
        """Dunder method for `<<` altering.

        Perform execution of `func` only when container is `Nothing`. In case container
        is `Some` just return it.

        Args:
            func (Callable[[TSome], Maybe[VSome]]): to alter.

        Returns:
            Maybe[VSome]: result.
        """
        match self:
            case Nothing():
                return func(None)
            case Some() as some:
                return some

    @staticmethod
    def bound(
        func: Callable[[TSome], "Maybe[VSome]"]
    ) -> Callable[["Maybe[TSome]"], "Maybe[VSome]"]:
        """Decorator for functions that will be executed only with `Some` value.

        Changes input type to `Maybe`.

        Example::

                @Maybe.bound
                def get_user(name: str) -> Maybe[User]:
                    ...

                result get_user(Nothing())  # Nothing
        """

        @wraps(func)
        def _bound(cnt: "Maybe[TSome]") -> "Maybe[VSome]":
            return cnt >> func

        return _bound

    @staticmethod
    def altered(
        func: Callable[[TSome], "Maybe[VSome]"]
    ) -> Callable[["Maybe[TSome]"], "Maybe[VSome]"]:
        """Decorator for functions that will be executed only with `Nothing`.

        Changes input type to `Maybe`.

        Example::

                @Maybe.bound
                def get_user(name: str) -> Maybe[User]:
                    ...

                result get_user(Nothing())  # Nothing
        """

        @wraps(func)
        def _altered(cnt: "Maybe[TSome]") -> "Maybe[VSome]":
            return cnt << func

        return _altered

    @staticmethod
    def _continue_on_some(
        cur: Callable[[TSome], VSome], nxt: Callable[[TSome], VSome]
    ) -> Callable[[TSome], VSome]:
        def __continue_on_some(val: TSome):
            match cur(val):
                case Some(result):
                    return result
                case Nothing():
                    return nxt(val)

        return __continue_on_some

    @staticmethod
    def choose(*funcs: Callable[[TSome], VSome]) -> Callable[[TSome], VSome]:
        """Return first `Some` result from passed functions.

        If `funcs` is empty, than return `Nothing`.
        If no `func` can return `Some` than return `Nothing`.

        Example::

                result = Some(1) >> choose(
                    lambda x: Nothing(),
                    lambda x: Some(2)
                )  # Some(2)
        """

        def _choose(value: TSome):
            match funcs:
                case ():
                    return Nothing()
                case _:
                    return reduce(Maybe._continue_on_some, funcs)(value)

        return _choose

    @staticmethod
    def no_none(
        func: Callable[[TSome], VSome | None]
    ) -> Callable[[TSome], "Maybe[VSome]"]:
        """Decorator for functions that might return `None`.

        When decorated function returns `None` it is converted to `Nothing`, otherwise
        wrapped into `Some` container.

        Example::

                @no_none
                def func(x: int) -> int | None:
                    return x if x > 10 else None

                Some(1) >> func  # Nothing
        """

        @wraps(func)
        def _wrapper(value: TSome):
            match func(value):
                case None:
                    return Nothing()
                case result:
                    return Some(result)

        return _wrapper


@dataclass(frozen=True)
class Some(Maybe[TSome]):
    """`Maybe` container for values that are actually present."""


@dataclass(frozen=True)
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
