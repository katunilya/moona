import pytest

from moona.http import HTTPContext, end
from moona.http.response_headers import (
    content_length,
    content_type,
    content_type_application_json,
    content_type_text_plain,
    header,
)


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s_value, b_value",
    [
        ("application/json", b"application/json"),
        ("text/plain", b"text/plain"),
        ("form/multipart", b"form/multipart"),
    ],
)
async def test_content_type(ctx: HTTPContext, s_value, b_value):
    _ctx = await content_type(s_value)(end, ctx)
    assert _ctx.response_headers[b"content-type"] == b_value


@pytest.mark.asyncio
async def test_content_type_application_json(ctx: HTTPContext):
    _ctx = await content_type_application_json(end, ctx)
    assert _ctx.response_headers[b"content-type"] == b"application/json"


@pytest.mark.asyncio
async def test_content_type_text_plain(ctx: HTTPContext):
    _ctx = await content_type_text_plain(end, ctx)
    assert _ctx.response_headers[b"content-type"] == b"text/plain"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "s_value, b_value",
    [
        (0, b"0"),
        (12, b"12"),
        (2355, b"2355"),
    ],
)
async def test_content_length(ctx: HTTPContext, s_value, b_value):
    _ctx = await content_length(s_value)(end, ctx)
    assert _ctx.response_headers[b"content-length"] == b_value
