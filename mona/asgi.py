from mona.core import (
    ASGIApp,
    ContextError,
    HTTPContext,
    LifespanContext,
    Receive,
    Scope,
    Send,
)
from mona.handlers.core import Handler, HTTPContextResult
from mona.handlers.error import send_error_async
from mona.handlers.events import send_body_async
from mona.monads.future import Future


def create(handler: Handler) -> ASGIApp:
    """Constructs ASGI Server function from passed handler.

    Supports 2 types of request scopes: "http" and "lifetime". For "http" scope
    `HTTPContext` is created and used as an argument for the `handler` (via `Future`).
    For "lifetime" `LifetimeContext` is created and also used as argument for `handler`.

    Notes:
        * https://asgi.readthedocs.io/en/latest/specs/main.html#applications

    Args:
        handler (Handler): function that executes on request and processes it.

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
                        await (Future.create(ctx) >> send_body_async)
                    case ContextError() as err:
                        await (Future.create(err) >> send_error_async)

    return _asgi
