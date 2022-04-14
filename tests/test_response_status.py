import pytest

from mona import context, future, res, state


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_status,assert_state,assert_status",
    [
        (state.RIGHT, res.status.ACCEPTED, state.RIGHT, res.status.ACCEPTED),
        (state.WRONG, res.status.ACCEPTED, state.WRONG, None),
    ],
)
async def test_set_status(
    mock_context: context.Context,
    arrange_state,
    arrange_status,
    assert_state,
    assert_status,
):
    # arrange
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_status(arrange_status)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    assert ctx.state == assert_state
    try:
        assert ctx.value.response.status == assert_status
    except AssertionError as e:
        if assert_state is state.RIGHT:
            raise e


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state, act_setter, assert_state, assert_status",
    [
        (state.RIGHT, res.set_status_ok, state.RIGHT, res.status.OK),
        (state.RIGHT, res.set_status_created, state.RIGHT, res.status.CREATED),
        (state.RIGHT, res.set_status_bad_request, state.RIGHT, res.status.BAD_REQUEST),
        (
            state.RIGHT,
            res.set_status_unauthorized,
            state.RIGHT,
            res.status.UNAUTHORIZED,
        ),
        (state.RIGHT, res.set_status_forbidden, state.RIGHT, res.status.FORBIDDEN),
        (state.RIGHT, res.set_status_not_found, state.RIGHT, res.status.NOT_FOUND),
        (
            state.RIGHT,
            res.set_status_method_not_allowed,
            state.RIGHT,
            res.status.METHOD_NOT_ALLOWED,
        ),
        (
            state.RIGHT,
            res.set_status_internal_server_error,
            state.RIGHT,
            res.status.INTERNAL_SERVER_ERROR,
        ),
        (
            state.RIGHT,
            res.set_status_not_implemented,
            state.RIGHT,
            res.status.NOT_IMPLEMENTED,
        ),
        (state.RIGHT, res.set_status_bad_gateway, state.RIGHT, res.status.BAD_GATEWAY),
        (state.WRONG, res.set_status_ok, state.WRONG, None),
        (state.WRONG, res.set_status_created, state.WRONG, None),
        (state.WRONG, res.set_status_bad_request, state.WRONG, None),
        (
            state.WRONG,
            res.set_status_unauthorized,
            state.WRONG,
            None,
        ),
        (state.WRONG, res.set_status_forbidden, state.WRONG, None),
        (state.WRONG, res.set_status_not_found, state.WRONG, None),
        (
            state.WRONG,
            res.set_status_method_not_allowed,
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            res.set_status_internal_server_error,
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            res.set_status_not_implemented,
            state.WRONG,
            None,
        ),
        (state.WRONG, res.set_status_bad_gateway, state.WRONG, None),
    ],
)
async def test_ready_setters(
    mock_context: context.Context,
    arrange_state,
    act_setter,
    assert_state,
    assert_status,
):
    # arrange
    ctx = future.from_value(state.pack(arrange_state, mock_context))

    # act
    ctx: context.StateContext = await (ctx >> act_setter)

    # assert
    assert ctx.state == assert_state

    try:
        assert ctx.value.response.status == assert_status
    except AssertionError as e:
        if assert_state is state.RIGHT:
            raise e
