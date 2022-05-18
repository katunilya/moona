from __future__ import annotations

from abc import ABC
from typing import Any, Awaitable, Callable

Message = dict[str, Any]
Scope = Message
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
ASGIData = tuple[Scope, Receive, Send]


class BaseContext(ABC):
    """Base class for each kind of Context handled by application.

    Mainly there are 3 kinds:
    * `HTTPContext` for "http" request scopes
    * `LifespanContext` for "lifetime" request scopes
    * `WebsocketContext` (not implemented)
    """

    send: Send
    receive: Receive
