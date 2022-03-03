from mona import future

from .types import ASGIContext, ASGIHandler, ASGIServer, Receive, Scope, Send


def create(*functions: ASGIHandler) -> ASGIServer:
    """Constructs ASGI Server function from sequence of handlers."""

    handler = future.compose(*functions)

    async def _asgi(scope: Scope, receive: Receive, send: Send) -> None:
        await handler(ASGIContext(scope, receive, send))

    return _asgi
