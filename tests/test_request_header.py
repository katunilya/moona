import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "raw_headers, parsed_headers",
    [
        ([[b"host", b"asgi-scope"]], {"host": "asgi-scope"}),
        (
            [
                [b"accept-language", b"en-US,en;q=0.5"],
                [b"accept-encoding", b"gzip, deflate, br"],
            ],
            {
                "accept-language": "en-US,en;q=0.5",
                "accept-encoding": "gzip, deflate, br",
            },
        ),
    ],
)
def test_parse_request_headers(
    asgi_context: context.Context,
    raw_headers,
    parsed_headers: dict[str, str],
):
    asgi_context.raw_headers = raw_headers
    ctx = req.parse_headers(asgi_context)
    assert ctx.request_headers == parsed_headers


@pytest.mark.parametrize(
    "headers,key,value,valid",
    [
        (
            [[b"Content-Type", b"application/json"]],
            "Content-Type",
            "application/json",
            True,
        ),
        (
            [[b"Content-Type", b"application/json"]],
            "Content-Type",
            "text/plain",
            False,
        ),
    ],
)
def test_on_header(
    asgi_context: context.Context,
    headers,
    key: str,
    value: str,
    valid: bool,
):
    asgi_context.raw_headers = headers
    handler_ = req.on_header(key, value)

    ctx = handler_(asgi_context)

    assert state.is_valid(ctx) is valid
