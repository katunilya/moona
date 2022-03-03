from typing import Awaitable, ByteString

from mona import future
from mona.types import Transform

from .types import ASGIContext, ASGIHandler


def set(body: ByteString) -> ASGIHandler:
    """Generates handler that sets response body from byte string."""

    def _handler(context: ASGIContext) -> ASGIContext:
        context.response_body = body
        return context

    return _handler


def set_text(text: str) -> ASGIHandler:
    """Generates handler that sets response body from Unicode string."""

    def _handler(context: ASGIContext) -> ASGIContext:
        context.response_body = text.encode("utf-8")
        return context

    return _handler


def set_from(handler: Transform[ASGIContext, Awaitable[ByteString]]) -> ASGIHandler:
    """Generates handler that sets response body from result of other function."""

    async def _handler(context: ASGIContext) -> ASGIContext:
        context.response_body = await future.bind(handler, context)
        return context

    return _handler
