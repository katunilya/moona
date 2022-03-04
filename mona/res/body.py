from typing import Awaitable, ByteString

from mona import context, future, types


def set_body(body: ByteString) -> context.Handler:
    """Generates handler that sets response body from byte string."""

    def _handler(ctx: context.Context) -> context.Context:
        ctx.response_body = body
        return ctx

    return _handler


def set_body_text(text: str) -> context.Handler:
    """Generates handler that sets response body from Unicode string."""

    def _handler(ctx: context.Context) -> context.Context:
        ctx.response_body = text.encode("utf-8")
        return ctx

    return _handler


def set_body_from(
    handler: types.Transform[context.Context, Awaitable[ByteString]]
) -> context.Handler:
    """Generates handler that sets response body from result of other function."""

    async def _handler(ctx: context.Context) -> context.Context:
        ctx.response_body = await future.bind(handler, ctx)
        return ctx

    return _handler
