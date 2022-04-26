from mona import handler, types
from mona.monads import state

GET = "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"
DELETE = "DELETE"
OPTIONS = "OPTIONS"
HEAD = "HEAD"
TRACE = "TRACE"
CONNECT = "CONNECT"


def on_method(method: str) -> handler.Handler:
    """Continue execution if request  method is passed method."""

    @state.accepts_right
    def _handler(ctx: types.Context) -> types.StateContext:
        return state.Right(ctx) if ctx.request.method == method else state.Wrong(ctx)

    return _handler


@state.accepts_right
def on_get(ctx: types.Context) -> types.StateContext:
    """Continue execution if request  method is `GET`."""
    return state.Right(ctx) if ctx.request.method == GET else state.Wrong(ctx)


@state.accepts_right
def on_post(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `POST`."""
    return state.Right(ctx) if ctx.request.method == POST else state.Wrong(ctx)


@state.accepts_right
def on_patch(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `PATCH`."""
    return state.Right(ctx) if ctx.request.method == PATCH else state.Wrong(ctx)


@state.accepts_right
def on_put(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `PUT`."""
    return state.Right(ctx) if ctx.request.method == PUT else state.Wrong(ctx)


@state.accepts_right
def on_delete(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `DELETE`."""
    return state.Right(ctx) if ctx.request.method == DELETE else state.Wrong(ctx)


@state.accepts_right
def on_options(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `OPTIONS`."""
    return state.Right(ctx) if ctx.request.method == OPTIONS else state.Wrong(ctx)


@state.accepts_right
def on_head(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `HEAD`."""
    return state.Right(ctx) if ctx.request.method == HEAD else state.Wrong(ctx)


@state.accepts_right
def on_trace(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `TRACE`."""
    return state.Right(ctx) if ctx.request.method == TRACE else state.Wrong(ctx)


@state.accepts_right
def on_connect(ctx: types.Context) -> types.StateContext:
    """Continue execution if request method is `CONNECT`."""
    return state.Right(ctx) if ctx.request.method == CONNECT else state.Wrong(ctx)
