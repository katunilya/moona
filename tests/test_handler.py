import inspect

import pytest

from mona import context, future, handler, state


def sync_handler(cnt: context.StateContext) -> context.StateContext:
    return cnt


async def async_handler(cnt: context.StateContext) -> context.StateContext:
    return cnt


def wrong_handler(cnt: context.StateContext) -> context.StateContext:
    return state.wrong(cnt.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "st, handlers, target_state",
    [
        (state.WRONG, [], state.WRONG),
        (state.WRONG, [wrong_handler], state.WRONG),
        (state.RIGHT, [wrong_handler], state.WRONG),
        (state.RIGHT, [wrong_handler, sync_handler], state.RIGHT),
        (state.RIGHT, [wrong_handler, async_handler], state.RIGHT),
        (state.RIGHT, [wrong_handler, sync_handler], state.RIGHT),
    ],
)
async def test_choose(
    mock_context: context.Context,
    st,
    handlers,
    target_state,
):
    ctx = future.from_value(state.State(mock_context, st))

    handler_ = handler.choose(*handlers)
    cnt = ctx >> handler_

    assert inspect.isawaitable(cnt)

    cnt: context.StateContext = await cnt

    assert cnt.state == target_state
