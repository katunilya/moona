import toolz

from mona import context, future, handler, state


def create(*handlers: handler.Handler) -> context.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers.

    Returns:
        context.ASGIServer: ASGI function
    """
    _handler = future.compose(*handlers)

    async def _asgi(
        scope: context.Scope,
        receive: context.Receive,
        send: context.Send,
    ) -> None:
        ctx = toolz.pipe(
            context.from_asgi(scope, receive, send),
            state.right,
            future.from_value,
            future.bind(_handler),
        )

        await ctx

    return _asgi
