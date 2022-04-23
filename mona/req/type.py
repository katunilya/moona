from mona import context
from mona.monads import state


@state.accepts_right
def on_http(ctx: context.Context) -> context.StateContext:
    """Returns right `Context` when request type is "http"."""
    return state.Right(ctx) if ctx.request.type_ == "http" else state.Wrong(ctx)
