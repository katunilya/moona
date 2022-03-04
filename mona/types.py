from typing import Any, Awaitable, Callable, Dict, TypeVar

from typing_extensions import TypeAlias

T = TypeVar("T")
V = TypeVar("V")


Transform: TypeAlias = Callable[[T], V]
Process: TypeAlias = Callable[[T], T]
Construct: TypeAlias = Callable[[], T]
Message: TypeAlias = Dict[str, Any]
Scope: TypeAlias = Message
Receive: TypeAlias = Construct[Awaitable[Message]]
Send: TypeAlias = Transform[Message, Awaitable[None]]
ASGIServer: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]
