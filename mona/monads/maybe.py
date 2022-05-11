from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Any, Awaitable, Callable, Generator, Generic, TypeVar

TSome = TypeVar("TSome")
VSome = TypeVar("VSome")


async def __this(x: TSome) -> TSome:
    return x


@dataclass(frozen=True, slots=True)
class FutureMaybe(Generic[TSome]):
    """Container for async optional value."""

    value: Awaitable[Maybe[TSome]]

    def __await__(self) -> Generator[None, None, Maybe[TSome]]:
        return self.value.__await__()

    async def __then(
        self, func: Callable[[TSome], Maybe[VSome]]
    ) -> Awaitable[Maybe[VSome]]:
        match await self.value:
            case Some(value):
                return func(value)
            case Nothing() as nothing:
                return nothing

    def then(self, func: Callable[[TSome], Maybe[VSome]]) -> FutureMaybe[VSome]:
        """Execute sync `func` if async value is `Some`.

        Args:
            func (Callable[[TSome], Maybe[VSome]]): to execute.

        Returns:
            FutureMaybe[VSome]: maybe result.
        """
        return FutureMaybe(self.__then(func))

    async def __otherwise(
        self, func: Callable[[Nothing], Maybe[VSome]]
    ) -> Awaitable[Maybe[VSome]]:
        match await self.value:
            case Nothing() as nothing:
                return func(nothing)
            case Some() as some:
                return some

    def otherwise(self, func: Callable[[Nothing], Maybe[VSome]]) -> FutureMaybe[VSome]:
        """Execute sync `func` if async value is `Nothing`.

        Args:
            func (Callable[[Nothing], Maybe[VSome]]): to execute.

        Returns:
            FutureMaybe[VSome]: maybe result.
        """
        return FutureMaybe(self.__otherwise(func))

    async def __then_future(
        self, func: Callable[[TSome], Awaitable[Maybe[VSome]]]
    ) -> Awaitable[Maybe[VSome]]:
        match await self.value:
            case Some(value):
                return await func(value)
            case Nothing() as nothing:
                return nothing

    def then_future(
        self, func: Callable[[TSome], Awaitable[Maybe[VSome]]]
    ) -> FutureMaybe[VSome]:
        """Execute async `func` if async value is `Some`.

        Args:
            func (Callable[[TSome], Awaitable[Maybe[VSome]]]): to execute.

        Returns:
            FutureMaybe[VSome]: maybe result.
        """
        return FutureMaybe(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[Nothing], Awaitable[Maybe[VSome]]]
    ) -> Maybe[VSome]:
        match await self.value:
            case Nothing() as nothing:
                return func(nothing)
            case Some() as some:
                return some

    def otherwise_future(
        self, func: Callable[[Nothing], Awaitable[Maybe[VSome]]]
    ) -> FutureMaybe[VSome]:
        """Execute async `func` if async value is `Nothing`.

        Args:
            func (Callable[[Nothing], Awaitable[Maybe[VSome]]]): to execute.

        Returns:
            FutureMaybe[VSome]: maybe result.
        """
        return FutureMaybe(self.__otherwise_future(func))

    @staticmethod
    def if_some(
        func: Callable[[TSome], Awaitable[Maybe[VSome]]]
    ) -> Callable[[Maybe[TSome]], Awaitable[Maybe[VSome]]]:
        """Decorator for async `func` to run only on `Some`."""

        @wraps(func)
        def _wrapper(cnt: Maybe[TSome]) -> Awaitable[Maybe[VSome]]:
            match cnt:
                case Some(value):
                    return func(value)
                case Nothing() as nothing:
                    return __this(nothing)

        return _wrapper

    @staticmethod
    def if_nothing(
        func: Callable[[Nothing], Awaitable[Maybe[VSome]]]
    ) -> Callable[[Maybe[TSome]], Awaitable[Maybe[VSome]]]:
        """Decorator for async `func` to run only on `Nothing`."""

        @wraps(func)
        def _wrapper(cnt: Maybe[TSome]) -> Awaitable[Maybe[VSome]]:
            match cnt:
                case Some() as some:
                    return __this(some)
                case Nothing(value):
                    return func(value)

        return _wrapper

    @staticmethod
    def returns(
        func: Callable[[TSome], Awaitable[VSome | None]]
    ) -> Callable[[TSome], Awaitable[Maybe[VSome]]]:
        """Decorator for functions that return `None` to return `Nothing` instead."""

        @wraps(func)
        async def _wrapper(arg: TSome) -> Maybe[VSome]:
            match await func(arg):
                case None:
                    return Nothing()
                case value:
                    return Some(value)

        return _wrapper

    @staticmethod
    def if_some_returns(
        func: Callable[[TSome], Awaitable[VSome | None]]
    ) -> Callable[[Maybe[TSome]], Awaitable[Maybe[VSome]]]:
        """Decorater that combines `if_some` and `returns`."""
        return FutureMaybe.if_some(FutureMaybe.returns(func))

    @staticmethod
    def if_nothing_returns(
        func: Callable[[Nothing], Awaitable[VSome | None]]
    ) -> Callable[[Nothing], Awaitable[Maybe[VSome]]]:
        """Decorater that combines `if_some` and `returns`."""
        return FutureMaybe.if_nothing(FutureMaybe.returns(func))


@dataclass(frozen=True, slots=True)
class Maybe(Generic[TSome], ABC):
    """General purpose container for optional value.

    `Maybe` container has 2 variations: `Some` and `Nothing`. `Some` stands for some
    actual value and means that it is present in execution context. `Nothing` on the
    other hand describes emptiness and lack of value. This is additional wrapping around
    `None` values.

    Example::

            user = {
                "name": "John Doe"
                "emails": {
                    "primary_email": "john_doe@example.com",
                }
            }

            primary_email = (
                Some(user)
                .then(get("emails"),)
                .then(get("primary_email"))
                .otherwise(empty_str)
            )  # Some("john_doe@example.com")

            primary_email = (
                Some(user)
                .then(get("emails"),)
                .then(get("primary_email"))
                .otherwise(empty_str)
            )  # Some("")
    """

    value: TSome

    def then(self, func: Callable[[TSome], Maybe[VSome]]) -> Maybe[VSome]:
        """Execute sync `func` if value is `Some`.

        Args:
            func (Callable[[TSome], Maybe[VSome]]): to execute.

        Returns:
            Maybe[VSome]: maybe result.
        """
        match self:
            case Some(value):
                return func(value)
            case Nothing() as nothing:
                return nothing

    def otherwise(self, func: Callable[[Nothing], Maybe[VSome]]) -> Maybe[VSome]:
        """Execute sync `func` if value is `Nothing`.

        Args:
            func (Callable[[Nothing], Maybe[VSome]]): to execute.

        Returns:
            Maybe[VSome]: maybe result.
        """
        match self:
            case Nothing():
                return func(None)
            case Some() as some:
                return some

    async def __then_future(
        self, func: Callable[[TSome], Awaitable[Maybe[VSome]]]
    ) -> Maybe[VSome]:
        match self:
            case Some(value):
                return await func(value)
            case Nothing() as nothing:
                return nothing

    def then_future(
        self, func: Callable[[TSome], Awaitable[Maybe[VSome]]]
    ) -> FutureMaybe[VSome]:
        """Execute async `func` if value is `Some` and return `FutureMaybe`.

        Args:
            func (Callable[[TSome], Awaitable[Maybe[VSome]]]): to execute.

        Returns:
            FutureMaybe[VSome]: result.
        """
        return FutureMaybe(self.__then_future(func))

    async def __otherwise_future(
        self, func: Callable[[Nothing], Awaitable[Maybe[VSome]]]
    ) -> Maybe[VSome]:
        match self:
            case Nothing() as nothing:
                return await func(nothing)
            case Some() as some:
                return some

    def otherwise_future(
        self, func: Callable[[Nothing], Awaitable[Maybe[VSome]]]
    ) -> FutureMaybe[VSome]:
        """Execute async `func` if value is `Nothing` and return `FutureMaybe`.

        Args:
            func (Callable[[Nothing], Awaitable[Maybe[VSome]]]): to execute.

        Returns:
            FutureMaybe[VSome]: result.
        """
        return FutureMaybe(self.__otherwise_future(func))

    @staticmethod
    def if_some(
        func: Callable[[TSome], Maybe[VSome]]
    ) -> Callable[[Maybe[TSome]], Maybe[VSome]]:
        """Decorator for functions that will be executed only with `Some` value.

        Changes input type to `Maybe`.

        Example::

                @Maybe.if_some
                def get_user(name: str) -> Maybe[User]:
                    ...

                result get_user(Nothing())  # Nothing
        """

        @wraps(func)
        def _if_some(cnt: Maybe[TSome]) -> Maybe[VSome]:
            return cnt.then(func)

        return _if_some

    @staticmethod
    def if_nothing(
        func: Callable[[TSome], Maybe[VSome]]
    ) -> Callable[[Maybe[TSome]], Maybe[VSome]]:
        """Decorator for functions that will be executed only with `Nothing`.

        Changes input type to `Maybe`.

        Example::

                @Maybe.if_nothing
                def or_zero(_) -> Maybe[int]:
                    return Some(0)

                or_zero(Nothing())  # Some(0)
        """

        @wraps(func)
        def _if_nothing(cnt: Maybe[TSome]) -> Maybe[VSome]:
            return cnt.otherwise(func)

        return _if_nothing

    @staticmethod
    def returns(
        func: Callable[[TSome], VSome | None]
    ) -> Callable[[TSome], Maybe[VSome]]:
        """Decorator for functions that might return `None`.

        When decorated function returns `None` it is converted to `Nothing`, otherwise
        wrapped into `Some` container.

        Example::

                @Maybe.returns
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

    def unpack(self) -> TSome | None:
        """Unpacks underlying value of container."""
        match self:
            case Nothing():
                return None
            case Some(value):
                return value

    @staticmethod
    def this(value: TSome | None) -> Maybe[TSome]:
        """Wraps value into `Some` if value is not `None`, otherwise in `Nothing`.

        Args:
            value (TSome | None): value to wrap.

        Returns:
            Maybe[TSome]: result.
        """
        match value:
            case None:
                return Nothing()
            case _:
                return Some(value)

    def otherwise_replace(self, value: VSome) -> Some[TSome] | Some[VSome]:
        """If this container is `Nothing` than replace it with `Some` value.

        Args:
            value (VSome): to replace with

        Returns:
            Some[TSome] | Some[VSome]: result.
        """
        match self:
            case Some():
                return self
            case Nothing():
                return Some(value)

    def return_some_or(self, value: VSome) -> TSome | VSome:
        """Return underlying value if self is `Some` or passed value.

        Combination of otherwise_replace and unpack that guarantees that `Some` is
        returned.

        Args:
            value (VSome): to return if self is `Nothing`.

        Returns:
            TSome | VSome: some result.
        """
        match self:
            case Nothing():
                return value
            case Some(internal_value):
                return internal_value


@dataclass(frozen=True, slots=True)
class Some(Maybe[TSome]):
    """`Maybe` container for values that are actually present."""


@dataclass(frozen=True, slots=True)
class Nothing(Maybe[Any]):
    """Singleton `Maybe` container marking value absence."""

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


# Utility functions


def if_dict_not_empty(data: dict) -> Maybe[dict]:  # noqa
    match data:
        case {}:
            return Nothing()
        case values:
            return Some(values)


def if_list_not_empty(data: list) -> Maybe[list]:  # noqa
    match data:
        case []:
            return Nothing()
        case values:
            return Some(values)
