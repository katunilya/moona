from mona import types
from mona.monads import state


@state.accepts_right
def on_http(ctx: types.Context) -> types.StateContext:
    """Returns right `Context` when request type is "http"."""
    return state.Right(ctx) if ctx.request.type_ == "http" else state.Wrong(ctx)
