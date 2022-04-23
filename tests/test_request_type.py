import pytest

from mona import context, req
from mona.monads import state


@pytest.mark.parametrize(
    "arrange_type,arrange_state,assert_state",
    [
        ("http", state.Right, state.Right),
        ("websocket", state.Right, state.Wrong),
        ("http", state.Wrong, state.Wrong),
        ("websocket", state.Wrong, state.Wrong),
    ],
)
def test_reqest_on_type(
    mock_context: context.Context, arrange_type, arrange_state, assert_state
):
    # arrange
    mock_context.request.type_ = arrange_type
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: context.StateContext = req.on_http(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
