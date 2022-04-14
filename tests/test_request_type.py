import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "arrange_type,arrange_state,assert_state",
    [
        ("http", state.RIGHT, state.RIGHT),
        ("websocket", state.RIGHT, state.WRONG),
        ("http", state.WRONG, state.WRONG),
        ("websocket", state.WRONG, state.WRONG),
    ],
)
def test_reqest_on_type(
    mock_context: context.Context, arrange_type, arrange_state, assert_state
):
    # arrange
    mock_context.request.type_ = arrange_type
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_http(ctx)

    # assert
    assert ctx.state == assert_state
