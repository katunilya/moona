from typing import Callable, TypeVar

from typing_extensions import TypeAlias

T = TypeVar("T")
V = TypeVar("V")


Transform: TypeAlias = Callable[[T], V]
Process: TypeAlias = Callable[[T], T]
Construct: TypeAlias = Callable[[], T]
