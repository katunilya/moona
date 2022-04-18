import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "arrange_headers,arrange_state,arrange_key,arrange_value,assert_state",
    [
        (
            {"content-type": b"application/json"},
            state.Right,
            "Content-Type",
            "application/json",
            state.Right,
        ),
        (
            {"content-type": b"application/json"},
            state.Right,
            "content-type",
            "application/json",
            state.Right,
        ),
        (
            {"content-type": b"application/json"},
            state.Wrong,
            "Content-Type",
            "application/json",
            state.Wrong,
        ),
        (
            {"content-type": b"application/json"},
            state.Right,
            "Content-Type",
            "text/plain",
            state.Wrong,
        ),
        (
            {"content-type": b"application/json"},
            state.Right,
            "Custom-Header",
            "some value",
            state.Wrong,
        ),
    ],
)
def test_on_header(
    mock_context: context.Context,
    arrange_headers,
    arrange_state,
    arrange_key,
    arrange_value,
    assert_state,
):
    # arrange
    mock_context.request.headers = arrange_headers
    arrange_handler = req.has_header(arrange_key, arrange_value)
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_headers,assert_state,assert_headers",
    [
        (
            {},
            state.Right,
            {},
        ),
        (
            {"content-type": b"application/json"},
            state.Right,
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
            state.Right,
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
    # arrange
    mock_context.request.headers = arrange_headers

    # act
    act_headers: state.State[dict[str, str]] = req.take_headers(mock_context)

    # assert
    assert isinstance(act_headers, assert_state)
    assert act_headers.value == assert_headers
