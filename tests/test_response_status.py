import pytest

from mona import context, res
from mona.monads import future, state


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_status,assert_state,assert_status",
    [
        (state.Right, res.status.ACCEPTED, state.Right, res.status.ACCEPTED),
        (state.Wrong, res.status.ACCEPTED, state.Wrong, None),
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
    ctx = future.from_value(arrange_state(mock_context))
    handler = res.set_status(arrange_status)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    assert isinstance(ctx, assert_state)
    try:
        assert ctx.value.response.status == assert_status
    except AssertionError as e:
        if assert_state is state.Right:
            raise e


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state, act_setter, assert_state, assert_status",
    [
        (state.Right, res.set_status_ok, state.Right, res.status.OK),
        (state.Right, res.set_status_created, state.Right, res.status.CREATED),
        (state.Right, res.set_status_bad_request, state.Right, res.status.BAD_REQUEST),
        (
            state.Right,
            res.set_status_unauthorized,
            state.Right,
            res.status.UNAUTHORIZED,
        ),
        (state.Right, res.set_status_forbidden, state.Right, res.status.FORBIDDEN),
        (state.Right, res.set_status_not_found, state.Right, res.status.NOT_FOUND),
        (
            state.Right,
            res.set_status_method_not_allowed,
            state.Right,
            res.status.METHOD_NOT_ALLOWED,
        ),
        (
            state.Right,
            res.set_status_internal_server_error,
            state.Right,
            res.status.INTERNAL_SERVER_ERROR,
        ),
        (
            state.Right,
            res.set_status_not_implemented,
            state.Right,
            res.status.NOT_IMPLEMENTED,
        ),
        (state.Right, res.set_status_bad_gateway, state.Right, res.status.BAD_GATEWAY),
        (state.Wrong, res.set_status_ok, state.Wrong, None),
        (state.Wrong, res.set_status_created, state.Wrong, None),
        (state.Wrong, res.set_status_bad_request, state.Wrong, None),
        (
            state.Wrong,
            res.set_status_unauthorized,
            state.Wrong,
            None,
        ),
        (state.Wrong, res.set_status_forbidden, state.Wrong, None),
        (state.Wrong, res.set_status_not_found, state.Wrong, None),
        (
            state.Wrong,
            res.set_status_method_not_allowed,
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            res.set_status_internal_server_error,
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            res.set_status_not_implemented,
            state.Wrong,
            None,
        ),
        (state.Wrong, res.set_status_bad_gateway, state.Wrong, None),
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
    ctx = future.from_value(arrange_state(mock_context))

    # act
    ctx: context.StateContext = await (ctx >> act_setter)

    # assert
    assert isinstance(ctx, assert_state)

    try:
        assert ctx.value.response.status == assert_status
    except AssertionError as e:
        if assert_state is state.Right:
            raise e
