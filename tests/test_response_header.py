import pytest

from mona import context, future, res, state


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "arrange_state,"
        "arrange_header_key,"
        "arrange_header_value,"
        "assert_state,"
        "assert_header_key,"
        "assert_header_value"
    ),
    [
        (
            state.Right,
            "Content-Type",
            "application/json",
            state.Right,
            b"Content-Type",
            b"application/json",
        ),
        (state.Wrong, "Content-Type", "application/json", state.Wrong, None, None),
    ],
)
async def test_set_header(
    mock_context: context.Context,
    arrange_state,
    arrange_header_key,
    arrange_header_value,
    assert_state,
    assert_header_key,
    assert_header_value,
):
    # arrange
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_header(arrange_header_key, arrange_header_value)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    try:
        assert isinstance(act_ctx, assert_state)
        assert act_ctx.value.response.headers[assert_header_key] == assert_header_value
    except KeyError:
        ...


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_value,assert_state,assert_value",
    [
        (state.Right, "application/json", state.Right, b"application/json"),
        (state.Wrong, "application/json", state.Wrong, None),
    ],
)
async def test_set_content_type(
    mock_context: context.Context,
    arrange_state,
    arrange_value,
    assert_state,
    assert_value,
):
    # arrange
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_header_content_type(arrange_value)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    try:
        assert isinstance(act_ctx, assert_state)
        assert act_ctx.value.response.headers[b"Content-Type"] == assert_value
    except KeyError:
        ...


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_setter,assert_state,assert_header_key,assert_header_value",
    [
        (
            state.Right,
            res.set_header_content_type_application_json,
            state.Right,
            b"Content-Type",
            b"application/json",
        ),
        (
            state.Wrong,
            res.set_header_content_type_application_json,
            state.Wrong,
            None,
            None,
        ),
        (
            state.Right,
            res.set_header_content_type_text_plain,
            state.Right,
            b"Content-Type",
            b"text/plain",
        ),
        (
            state.Wrong,
            res.set_header_content_type_text_plain,
            state.Wrong,
            None,
            None,
        ),
    ],
)
async def test_ready_setters(
    mock_context: context.Context,
    arrange_state,
    act_setter,
    assert_state,
    assert_header_key,
    assert_header_value,
):
    # arrange
    arrange_ctx = future.from_value(arrange_state(mock_context))

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> act_setter)

    # assert
    try:
        assert isinstance(act_ctx, assert_state)
        assert act_ctx.value.response.headers[assert_header_key] == assert_header_value
    except KeyError:
        ...
