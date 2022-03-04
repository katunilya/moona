import inspect

import pytest
from mona import handler, context, state


def sync_handler(context_: context.Context) -> context.Context:
    return context_


async def async_handler(context_: context.Context) -> context.Context:
    return context_


def invalid_handler(x):
    return state.invalid(x)


@pytest.mark.asyncio
async def test_compose(asgi_context):
    _handler = handler.compose(
        sync_handler,
        async_handler,
        sync_handler,
        async_handler,
        invalid_handler,
        async_handler,
        async_handler,
        async_handler,
    )

    ctx = _handler(asgi_context)

    assert inspect.isawaitable(ctx)

    ctx = await ctx

    assert isinstance(ctx, state.State)
    assert ctx.valid is False


@pytest.mark.asyncio
async def test_choose(asgi_context):
    def invalid_handler(x):
        return state.invalid(x)

    def valid_handler(x):
        return state.valid(x)

    def simple_handler(x):
        return x

    _handler = handler.choose(
        invalid_handler,
        handler.compose(
            valid_handler,
            simple_handler,
        ),
    )

    ctx = context.bind(_handler, asgi_context)

    assert inspect.isawaitable(ctx)

    ctx = await ctx

    assert isinstance(ctx, state.State)
    assert ctx.valid
