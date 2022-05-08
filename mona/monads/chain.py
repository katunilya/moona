from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, TypeVar

from mona.monads.future import Future

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")


@dataclass(slots=True)
class FutureChain(Generic[X, Y]):
    """Async function composition abstraction."""

    value: Callable[[X], Awaitable[Y]]

    def __call__(self, arg: X) -> Awaitable[Y]:  # noqa
        return self.value(arg)

    def then(self, func: Callable[[Y], Z]) -> "FutureChain[X, Z]":
        """Compose this function with the sync next one sequentially.

        Args:
            func (Callable[[Y], Z]): to compose with.

        Returns:
            FutureChain[X, Z]: result function.
        """

        def _then(arg: X) -> Future[Z]:
            return Future(self(arg)).then(func)

        return FutureChain(_then)

    def then_future(self, func: Callable[[Y]]) -> "FutureChain[X, Z]":
        """Compose this function with the async next one sequentially.

        Args:
            self (Callable[[Y], Awaitable[Z]]): to compose with.

        Returns:
            FutureChain[X, Z]: result function.
        """

        def _then_future(arg: X) -> Future[Z]:
            return Future(self(arg)).then_future(func)

        return FutureChain(_then_future)


@dataclass(slots=True)
class Chain(Generic[X, Y]):
    """Sync function composition abstraction.

    Compatible with `FutureChain`.
    """

    value: Callable[[X], Y]

    def __call__(self, arg: X) -> Y:  # noqa
        return self.value(arg)

    def then(self, func: Callable[[Y], Z]) -> "Chain[X, Z]":
        """Compose this function with the sync next one sequentially.

        Args:
            func (Callable[[Y], Z]): to compose with.

        Returns:
            Chain[X, Z]: result function.
        """

        def _then(arg: X) -> Z:
            return func(self(arg))

        return Chain(_then)

    def then_future(self, func: Callable[[Y], Awaitable[Z]]) -> "FutureChain[X, Z]":
        """Compose this function with the async next one sequentially.

        Args:
            func (Callable[[Y], Awaitable[Z]]): to compose with.

        Returns:
            FutureChain[X, Z]: result function.
        """

        def _then_future(arg: X) -> Future[Z]:
            return Future(func(self(arg)))

        return FutureChain(_then_future)
