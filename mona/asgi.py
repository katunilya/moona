import toolz

from mona import context, future, handler, state


def create(handler: handler.Handler) -> context.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers.

    Returns:
        context.ASGIServer: ASGI function
    """

    async def _asgi(
        scope: context.Scope,
        receive: context.Receive,
        send: context.Send,
    ) -> None:
        ctx = toolz.pipe(
            context.from_asgi(scope, receive, send),
            state.right,
            future.from_value,
        )

        await (ctx >> handler)

    return _asgi
