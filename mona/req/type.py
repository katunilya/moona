from mona import context, state


def on_http(ctx: context.Context) -> context.StateContext:
    """Returns valid `Context` when request type is `http`."""
    return state.valid(ctx) if ctx.type == "http" else state.invalid(ctx)
