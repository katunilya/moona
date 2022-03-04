import inspect

import pytest

from mona import context, state


def sync_handler(context_: context.Context) -> context.Context:
    return context_


async def async_handler(context_: context.Context) -> context.Context:
    return context_


@pytest.mark.asyncio
async def test_pack(asgi_context: context.Context):

    asgi_context = context.pack(asgi_context)

    assert inspect.isawaitable(asgi_context)

    asgi_context = await asgi_context

    assert isinstance(asgi_context, state.State)


@pytest.mark.asyncio
async def test_multiple_pack(asgi_context: context.Context):

    asgi_context = context.pack(context.pack(asgi_context))

    assert inspect.isawaitable(asgi_context)

    asgi_context = await asgi_context

    assert isinstance(asgi_context, state.State)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "handler, valid",
    [
        (async_handler, True),
        (sync_handler, True),
    ],
)
async def test_bind(
    asgi_context: context.Context, handler: context.Handler, valid: bool
):
    ctx = context.bind(handler, asgi_context)
    assert inspect.isawaitable(ctx)

    ctx = await ctx

    assert isinstance(ctx, state.State)
    assert ctx.valid == valid
