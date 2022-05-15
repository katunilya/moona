from moona import http, lifespan
from moona.context import ASGIApp, Receive, Scope, Send

_default_http_handler = http.send_text("Empty server")


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
        http (AsyncHTTPContextHandler): handler for "http" scope
        lifespan (AsyncLifespanContextHandler): handler for "lifespan" scope

    Returns:
        ASGIApp: ASGI function based on ASGI Specification.
    """

    async def _asgi(scope: Scope, receive: Receive, send: Send) -> None:
        match scope:
            case {"type": "lifespan"}:
                ctx = lifespan.LifespanContext(scope, receive, send)
                while True:
                    match await ctx.receive():
                        case {"type": "lifespan.startup"}:
                            match startup_handler:
                                case None:
                                    await ctx.send(
                                        {"type": "lifespan.startup.complete"}
                                    )
                                case _:
                                    await startup_handler(lifespan.end, ctx)
                                    await ctx.send(
                                        {"type": "lifespan.startup.complete"}
                                    )
                        case {"type": "lifespan.shutdown"}:
                            match shutdown_handler:
                                case None:
                                    await ctx.send(
                                        {"type": "lifespan.shutdown.complete"}
                                    )
                                case _:
                                    await shutdown_handler(lifespan.end, ctx)
                                    await ctx.send(
                                        {"type": "lifespan.shutdown.complete"}
                                    )
                            return
            case {"type": "http"}:
                ctx = http.HTTPContext(scope, receive, send)
                await http_handler(http.end, ctx)

    return _asgi
