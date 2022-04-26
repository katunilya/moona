import inspect

import pytest

from mona import handler, types
from mona.monads import future, state


def sync_handler(cnt: types.StateContext) -> types.StateContext:
    return cnt


async def async_handler(cnt: types.StateContext) -> types.StateContext:
    return cnt


def wrong_handler(cnt: types.StateContext) -> types.StateContext:
    return state.Wrong(cnt.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_handlers,assert_state",
    [
        (state.Wrong, [], state.Wrong),
        (state.Right, [], state.Right),
        (state.Wrong, [wrong_handler], state.Wrong),
        (state.Right, [wrong_handler], state.Wrong),
        (state.Right, [wrong_handler, sync_handler], state.Right),
        (state.Right, [wrong_handler, async_handler], state.Right),
        (state.Right, [wrong_handler, sync_handler], state.Right),
    ],
)
async def test_choose(
    mock_context: types.Context,
    arrange_state,
    arrange_handlers,
    assert_state,
):
    # act
    act_ctx = (
        arrange_state(mock_context)
        >> future.from_value
        >> handler.choose(*arrange_handlers)
    )

    # asset
    assert inspect.isawaitable(act_ctx)

    # act
    act_ctx: types.StateContext = await act_ctx

    # assert
    assert isinstance(act_ctx, assert_state)
