from mona import handler, types
from mona.monads import future, state


def create(handler: handler.Handler) -> types.ASGIServer:
    """Constructs ASGI Server function from sequence of handlers.

    Returns:
        context.ASGIServer: ASGI function
    """

    async def _asgi(
        scope: types.Scope, receive: types.Receive, send: types.Send
    ) -> None:
        await (
            future.from_value((scope, receive, send))
            >> types.from_asgi
            >> state.Right
            >> handler
        )

    return _asgi
