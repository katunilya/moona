from functools import reduce, wraps

from mona import context, state, types


def wrap(handler: types.Transform[context.Context, context.Context]) -> context.Handler:
    """Decorates function so that it operates as `context.Handler`."""

    @wraps(handler)
    def _wrapper(ctx: context.Context) -> context.StateContext:
        return context.bind(handler, ctx)

    return _wrapper


def compose(*handlers: context.Handler) -> context.Handler:
    """Commposes multiple `context.Handler`s into one."""

    @wrap
    def _compose(ctx: context.FutureStateContext) -> context.StateContext:
        return reduce(lambda c, h: context.bind(h, c), handlers, ctx)

    return _compose


def choose(*handlers: context.Handler) -> context.Handler:
    """First `context.Handler` to return valid result is executed."""

    @wrap
    async def _choose(ctx: context.FutureStateContext) -> context.StateContext:
        for handler in handlers:
            _ctx: context.StateContext = await context.bind(handler, ctx)

            if isinstance(_ctx, state.Valid):
                return _ctx

        return ctx

    return _choose
