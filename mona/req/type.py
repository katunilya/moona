from mona import context, state


@state.accepts_right
def on_http(ctx: context.Context) -> context.StateContext:
    """Returns right `Context` when request type is "http"."""
    return state.right(ctx) if ctx.request.type_ == "http" else state.wrong(ctx)
