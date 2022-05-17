from moona import http, lifespan
from moona.context import ASGIApp, Receive, Scope, Send


async def _handle_lifespan(
    scope: Scope,
    receive: Receive,
    send: Send,
    *,
    startup_handler: lifespan.LifespanHandler = None,
    shutdown_handler: lifespan.LifespanHandler = None,
) -> None:
    ctx = lifespan.LifespanContext(scope, receive, send)
    while True:
        match await ctx.receive():
            case {"type": "lifespan.startup"}:
                match startup_handler:
                    case None:
                        await ctx.send({"type": "lifespan.startup.complete"})
                    case _:
                        await startup_handler(lifespan.end, ctx)
                        await ctx.send({"type": "lifespan.startup.complete"})
            case {"type": "lifespan.shutdown"}:
                match shutdown_handler:
                    case None:
                        await ctx.send({"type": "lifespan.shutdown.complete"})
                    case _:
                        await shutdown_handler(lifespan.end, ctx)
                        await ctx.send({"type": "lifespan.shutdown.complete"})
                return


_default_http_handler = http.not_implemented("Service is not implemented. Sorry!")


async def _handle_http(
    scope: Scope,
    receive: Receive,
    send: Send,
    *,
    http_handler: http.HTTPHandler = None,
):
    ctx = http.HTTPContext(scope, receive, send)
    await http_handler(http.end, ctx)


def create(
    *,
    http_handler: http.HTTPHandler = _default_http_handler,
    startup_handler: lifespan.LifespanHandler = None,
    shutdown_handler: lifespan.LifespanHandler = None,
) -> ASGIApp:
    """Constructs ASGI Server function from passed handler.

    Supports 2 types of request scopes: "http" and "lifetime". For "http" scope
    `HTTPContext` is created and used as an argument for the `handler` (via `Future`).
    For "lifetime" `LifetimeContext` is created and also used as argument for `handler`.

    Notes:
        * https://asgi.readthedocs.io/en/latest/specs/main.html#applications

    Args:
        http_handler (HTTPHandler): optional argument for handling "http" requests.
        on_startup_handler (LifespanHandler): optional for handlers to be executed on
        server startup
        on_shutdown_handler (LifespanHandler): optional for handlers to be executed on
        server shutdown

    Returns:
        ASGIApp: ASGI function based on ASGI Specification.
    """

    async def _asgi(scope: Scope, receive: Receive, send: Send) -> None:
        match scope:
            case {"type": "lifespan"}:
                await _handle_lifespan(
                    scope,
                    receive,
                    send,
                    startup_handler=startup_handler,
                    shutdown_handler=shutdown_handler,
                )
            case {"type": "http"}:
                await _handle_http(
                    scope,
                    receive,
                    send,
                    http_handler=http_handler,
                )

    return _asgi
