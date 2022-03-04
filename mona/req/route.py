from mona import context, state


def on_route(path: str) -> context.Handler:
    """If `path` is the same as request `path` than context is valid."""

    def _handler(ctx: context.Context) -> context.StateContext:
        return state.valid(ctx) if path == ctx.path else state.invalid(ctx)

    return _handler
