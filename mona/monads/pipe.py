from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, TypeVar

from mona.monads.future import Future
from mona.monads.result import Result, TBad, TOk

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
        """Execute passed function on `Pipe` object value and return next `Pipe`.

        Args:
            func (Callable[[X], Y]): to execute.

        Returns:
            Pipe[Y]: execution result.
        """
        return Pipe(func(self.value))

    def then_future(self, func: Callable[[X], Awaitable[Y]]) -> Future[Y]:
        """Execute passed async function on `Pipe` object value and return `Future`.

        Args:
            func (Callable[[X], Awaitable[Y]]): to execute.

        Returns:
            Future[Y]: execution result.
        """
        return Future(func(self.value))

    def then_result(self, func: Callable[[X], Result[TOk, TBad]]) -> Result[TOk, TBad]:
        """Execute passed sync function on `Pipe` object value and return `Result`.

        Args:
            func (Callable[[X], Result[TOk, TBad]]): to execute.

        Returns:
            Result[TOk, TBad]: _description_
        """
        return func(self.value)

    def unpack(self) -> X:
        """Return internal `Pipe` value.

        Returns:
            X: internal value.
        """
        return self.value
