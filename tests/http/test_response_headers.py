import pytest

from moona.http import HTTPContext, end, header


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s_name, s_value, b_name, b_value",
    [
        ("Content-Type", "application/json", b"content-type", b"application/json"),
        ("Content-type", "application/json", b"content-type", b"application/json"),
        ("content-type", "application/json", b"content-type", b"application/json"),
    ],
)
async def test_header(ctx: HTTPContext, s_name, s_value, b_name, b_value):
    _ctx = await header(s_name, s_value)(end, ctx)
    assert _ctx.response_headers[b_name] == b_value
