from toolz import pipe

from mona import context, future, handler


def create(*handlers: handler.Handler) -> context.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers.

    Returns:
        context.ASGIServer: ASGI function
    """
    _handler = handler.compose(*handlers)

    async def _asgi(
        scope: context.Scope,
        receive: context.Receive,
        send: context.Send,
    ) -> None:
        ctx: context.FutureStateContext = pipe(
            context.from_asgi(scope, receive, send),
            context.right,
            future.from_value,
        )

        await ctx >> _handler

    return _asgi
