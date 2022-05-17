import pytest

from moona.http import HTTPContext
from moona.http.handlers import end
from moona.http.request_headers import has_header, matches_header


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s_name, b_name, result",
    [
        ("content-type", b"content-type", True),
        ("content-Type", b"content-type", True),
        ("Content-type", b"content-type", True),
        ("Content-Type", b"content-type", True),
        ("Random-Header", b"", False),
    ],
)
async def test_has_header_1(ctx: HTTPContext, s_name, b_name, result):
    ctx.request_headers[b_name] = b""
    _ctx = await has_header(s_name)(end, ctx)
    assert (_ctx is not None) == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s_name, s_value, b_name, b_value, result",
    [
        (
            "content-type",
            "application/json",
            b"content-type",
            b"application/json",
            True,
        ),
        (
            "content-Type",
            "text/plain",
            b"content-type",
            b"application/json",
            False,
        ),
        (
            "Content-type",
            "application/json",
            b"content-type",
            b"text/plain",
            False,
        ),
        ("Random-Header", "any", b"", b"", False),
    ],
)
async def test_matches_header(
    ctx: HTTPContext, s_name, s_value, b_name, b_value, result
):
    ctx.request_headers[b_name] = b_value
    _ctx = await matches_header(s_name, s_value)(end, ctx)
    assert (_ctx is not None) == result
