from mona import context, future, handler, state


def create(handler: handler.Handler) -> context.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers.

    Returns:
        context.ASGIServer: ASGI function
    """

    async def _asgi(
        scope: context.Scope, receive: context.Receive, send: context.Send
    ) -> None:
        await (
            future.from_value((scope, receive, send))
            >> context.from_asgi
            >> state.right
            >> handler
        )

    return _asgi
