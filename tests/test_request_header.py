import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "headers,init_state,header_key,header_value,target_state,",
    [
        (
            {"content-type": b"application/json"},
            state.RIGHT,
            "Content-Type",
            "application/json",
            state.RIGHT,
        ),
        (
            {"content-type": b"application/json"},
            state.RIGHT,
            "content-type",
            "application/json",
            state.RIGHT,
        ),
        (
            {"content-type": b"application/json"},
            state.WRONG,
            "Content-Type",
            "application/json",
            state.WRONG,
        ),
        (
            {"content-type": b"application/json"},
            state.RIGHT,
            "Content-Type",
            "text/plain",
            state.WRONG,
        ),
        (
            {"content-type": b"application/json"},
            state.RIGHT,
            "Custom-Header",
            "some value",
            state.WRONG,
        ),
    ],
)
def test_on_header(
    mock_context: context.Context,
    headers,
    init_state,
    header_key,
    header_value,
    target_state,
):
    mock_context.request.headers = headers
    handler_ = req.has_header(header_key, header_value)
    ctx = state.State(mock_context, init_state)

    ctx = handler_(ctx)

    assert ctx.state == target_state


@pytest.mark.parametrize(
    "arrange_headers,assert_state,assert_headers",
    [
        (
            {},
            state.RIGHT,
            {},
        ),
        (
            {"content-type": b"application/json"},
            state.RIGHT,
            {"content-type": "application/json"},
        ),
        (
            {
                "Connection": b"Keep-Alive",
                "Content-Encoding": b"gzip",
                "Content-Type": b"text/html; charset=utf-8",
                "Date": b"Thu, 11 Aug 2016 15:23:13 GMT",
                "Keep-Alive": b"timeout=5, max=1000",
            },
            state.RIGHT,
            {
                "Connection": "Keep-Alive",
                "Content-Encoding": "gzip",
                "Content-Type": "text/html; charset=utf-8",
                "Date": "Thu, 11 Aug 2016 15:23:13 GMT",
                "Keep-Alive": "timeout=5, max=1000",
            },
        ),
    ],
)
def test_take_headers(
    mock_context: context.Context,
    arrange_headers,
    assert_state,
    assert_headers,
):
    mock_context.request.headers = arrange_headers

    headers: state.State[dict[str, str]] = req.take_headers(mock_context)

    assert headers.state == assert_state
    assert headers.value == assert_headers
