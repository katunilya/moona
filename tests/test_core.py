import inspect

import pytest

from mona.context import Context
from mona.core import choose
from mona.monads import future
from mona.monads.maybe import Maybe, Nothing, Some


def sync_handler(ctx: Maybe[Context]) -> Maybe[Context]:
    return ctx


async def async_handler(ctx: Maybe[Context]) -> Maybe[Context]:
    return ctx


def wrong_handler(ctx: Maybe[Context]) -> Maybe[Context]:
    return Nothing()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,arrange_handlers,assert_state",
    [
        (Nothing, [], Nothing),
        (Some, [], Some),
        (Nothing, [wrong_handler], Nothing),
        (Some, [wrong_handler], Nothing),
        (Some, [wrong_handler, sync_handler], Some),
        (Some, [wrong_handler, async_handler], Some),
        (Some, [wrong_handler, sync_handler], Some),
    ],
)
async def test_choose(
    mock_context: Context,
    arrange_state,
    arrange_handlers,
    assert_state,
):
    match issubclass(arrange_state, Some):
        case True:
            arrange_ctx = Some(mock_context)
        case False:
            arrange_ctx = Nothing()
    # act
    act_ctx = future.from_value(arrange_ctx) >> choose(*arrange_handlers)

    # asset
    assert inspect.isawaitable(act_ctx)

    # act
    act_ctx: Maybe[Context] = await act_ctx

    # assert
    assert isinstance(act_ctx, assert_state)
