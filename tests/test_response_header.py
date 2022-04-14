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
            state.RIGHT,
            "Content-Type",
            "application/json",
            state.RIGHT,
            b"Content-Type",
            b"application/json",
        ),
        (state.WRONG, "Content-Type", "application/json", state.WRONG, None, None),
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
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_header(arrange_header_key, arrange_header_value)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    try:
        assert ctx.state == assert_state
        assert ctx.value.response.headers[assert_header_key] == assert_header_value
    except KeyError:
        # in case ctx.state == assert_state is not right
        ...


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_value,assert_state,assert_value",
    [
        (state.RIGHT, "application/json", state.RIGHT, b"application/json"),
        (state.WRONG, "application/json", state.WRONG, None),
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
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_header_content_type(arrange_value)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    try:
        assert ctx.state == assert_state
        assert ctx.value.response.headers[b"Content-Type"] == assert_value
    except KeyError:
        # in case ctx.state == assert_state is not right
        ...


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_setter,assert_state,assert_header_key,assert_header_value",
    [
        (
            state.RIGHT,
            res.set_header_content_type_application_json,
            state.RIGHT,
            b"Content-Type",
            b"application/json",
        ),
        (
            state.WRONG,
            res.set_header_content_type_application_json,
            state.WRONG,
            None,
            None,
        ),
        (
            state.RIGHT,
            res.set_header_content_type_text_plain,
            state.RIGHT,
            b"Content-Type",
            b"text/plain",
        ),
        (
            state.WRONG,
            res.set_header_content_type_text_plain,
            state.WRONG,
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
    ctx = future.from_value(state.pack(arrange_state, mock_context))

    # act
    ctx: context.StateContext = await (ctx >> act_setter)

    # assert
    try:
        assert ctx.state == assert_state
        assert ctx.value.response.headers[assert_header_key] == assert_header_value
    except KeyError:
        # in case ctx.state == assert_state is not right
        ...
