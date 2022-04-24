import abc
import dataclasses
from typing import Generic, TypeVar

TValue = TypeVar("TValue")


@dataclasses.dataclass(frozen=True)
class Container(abc.ABC, Generic[TValue]):
    """Base container class for different monads.

    Any monad has a container which explicitly shows what object we actually operate.
    For that we specifically have this concrete abstract `Container` class. Monad
    containers should be immutable, however it does not guarantee that wrapped `value`
    is immutable too.
    """

    value: TValue
