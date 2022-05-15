import pytest

from moona.context import ErrorContext, HTTPContext
from moona.handlers.error import send_error_async


@pytest.mark.asyncio
async def test_send_error_async(ctx: HTTPContext):
    ctx = await (ErrorContext(ctx, "Unauthorized", 501) >> send_error_async)
    assert ctx.response.body == b"Unauthorized"
    assert ctx.response.status == 501
    assert ctx.response.headers[b"content-type"] == b"text/plain"
    assert ctx.response.headers[b"content-length"] == b"12"
    assert ctx.started is True
    assert ctx.closed is True
