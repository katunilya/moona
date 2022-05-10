from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, TypeVar

from mona.monads.future import Future
from mona.monads.maybe import FutureMaybe, Maybe
from mona.monads.result import FutureResult, Result, TError, TOk

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")


@dataclass(slots=True)
class Pipe(Generic[X]):
    """Abstraction for creating pipelines with sync and async functions.

    Sync equivalent of `Future` with compatibility features.
    """

    value: X

    def then(self, func: Callable[[X], Y]) -> "Pipe[Y]":
        """Execute passed sync `func` on `Pipe` value and return next `Pipe`.

        Args:
            func (Callable[[X], Y]): to execute.

        Returns:
            Pipe[Y]: execution result.
        """
        return Pipe(func(self.value))

    def then_future(self, func: Callable[[X], Awaitable[Y]]) -> Future[Y]:
        """Execute passed async `func` on `Pipe` value and return `Future`.

        Args:
            func (Callable[[X], Awaitable[Y]]): to execute.

        Returns:
            Future[Y]: execution result.
        """
        return Future(func(self.value))

    def then_result(
        self, func: Callable[[X], Result[TOk, TError]]
    ) -> Result[TOk, TError]:
        """Execute passed sync `func` on `Pipe` value and return `Result`.

        Args:
            func (Callable[[X], Result[TOk, TBad]]): to execute.

        Returns:
            Result[TOk, TBad]: result.
        """
        return func(self.value)

    def then_maybe(self, func: Callable[[X], Maybe[Y]]) -> Maybe[Y]:
        """Execute passed sync `func` on `Pipe` value and return `Maybe`.

        Args:
            func (Callable[[X], Maybe[Y]]): to execute.

        Returns:
            Maybe[Y]: result.
        """
        return func(self.value)

    def then_future_result(
        self, func: Callable[[X], Awaitable[Result[TOk, TError]]]
    ) -> FutureResult[TOk, TError]:
        """Execute passed async `func` on `Pipe` value and return `FutureResult`.

        Args:
            func (Callable[[X], Awaitable[Result[TOk, TBad]]]): to execute.

        Returns:
            FutureResult[TOk, TBad]: future result.
        """
        return FutureResult(func(self.value))

    def then_future_maybe(
        self, func: Callable[[X], Awaitable[Maybe[Y]]]
    ) -> FutureMaybe[Y]:
        """Execute passed async `func` on `Pipe` value and return `MaybeFuture`.

        Args:
            func (Callable[[X], Awaitable[Maybe[Y]]]): to execute.

        Returns:
            FutureMaybe[Y]: future maybe.
        """
        return FutureMaybe(func(self.value))

    def unpack(self) -> X:
        """Return internal `Pipe` value.

        Returns:
            X: internal value.
        """
        return self.value

    @staticmethod
    def this(value: X) -> X:
        """Sync identity function."""
        return value
