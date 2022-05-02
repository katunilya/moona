from mona.core import (
    ASGIApp,
    ContextError,
    HTTPContext,
    LifespanContext,
    Receive,
    Scope,
    Send,
)
from mona.handlers.core import HTTPContextResult, HTTPHandler
from mona.handlers.error import send_error_async
from mona.handlers.events import send_body_async
from mona.monads.future import Future


def create(handler: HTTPHandler) -> ASGIApp:
    """Constructs ASGI Server function from sequence of handlers.

    Notes:
        * https://asgi.readthedocs.io/en/latest/specs/main.html#applications

    Returns:
        ASGIApp: ASGI function based on ASGI Specification.
    """

    async def _asgi(scope: Scope, receive: Receive, send: Send) -> None:
        match scope:
            case {"type": "lifespan"}:
                await (
                    Future.create(LifespanContext.create(scope, receive, send))
                    >> handler
                )
            case {"type": "http"}:
                result: HTTPContextResult = await (
                    Future.create(HTTPContext.create(scope, receive, send)) >> handler
                )
                match result:
                    case HTTPContext() as ctx:
                        await (ctx >> send_body_async)
                    case ContextError() as err:
                        await (err >> send_error_async)

    return _asgi
