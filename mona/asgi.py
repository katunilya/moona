from mona import context, handler, types


def create(*handlers: context.Handler) -> types.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers."""
    _handler = handler.compose(*handlers)

    async def _asgi(
        scope: types.Scope, receive: types.Receive, send: types.Send
    ) -> None:
        await _handler(context.Context(scope, receive, send))

    return _asgi
