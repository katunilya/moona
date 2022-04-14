from typing import Union

from mona import context, handler, state

GET = "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"
DELETE = "DELETE"
OPTIONS = "OPTIONS"
HEAD = "HEAD"
TRACE = "TRACE"
CONNECT = "CONNECT"

Method = Union[
    "GET",
    "POST",
    "PATCH",
    "PUT",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
    "CONNECT",
]


def on_method(method: Method) -> handler.Handler:
    """Continue execution if request  method is passed method."""

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        if ctx.request.method == method:
            return state.right(ctx)

        return state.wrong(ctx)

    return _handler


@state.accepts_right
def on_get(ctx: context.Context) -> context.StateContext:
    """Continue execution if request  method is `GET`."""
    if ctx.request.method == GET:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_post(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `POST`."""
    if ctx.request.method == POST:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_patch(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `PATCH`."""
    if ctx.request.method == PATCH:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_put(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `PUT`."""
    if ctx.request.method == PUT:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_delete(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `DELETE`."""
    if ctx.request.method == DELETE:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_options(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `OPTIONS`."""
    if ctx.request.method == OPTIONS:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_head(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `HEAD`."""
    if ctx.request.method == HEAD:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_trace(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `TRACE`."""
    if ctx.request.method == TRACE:
        return state.right(ctx)

    return state.wrong(ctx)


@state.accepts_right
def on_connect(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `CONNECT`."""
    if ctx.request.method == CONNECT:
        return state.right(ctx)

    return state.wrong(ctx)
