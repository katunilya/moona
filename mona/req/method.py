from typing import Union

from toolz.functoolz import pipe

from mona import context, state

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


def on_method(method: Method) -> context.Handler:
    """Continue executeion if request  method is passed method."""

    def _handler(ctx: context.Context) -> context.StateContext:
        return state.Valid(ctx) if ctx.method == method else state.Invalid(ctx)

    return _handler


def on_get(ctx: context.Context) -> context.StateContext:
    """Continue executeion if request  method is `GET`."""
    return pipe(ctx, on_method(GET))


def on_post(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `POST`."""
    return pipe(ctx, on_method(POST))


def on_patch(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `PATCH`."""
    return pipe(ctx, on_method(PATCH))


def on_put(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `PUT`."""
    return pipe(ctx, on_method(PUT))


def on_delete(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `DELETE`."""
    return pipe(ctx, on_method(DELETE))


def on_options(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `OPTIONS`."""
    return pipe(ctx, on_method(OPTIONS))


def on_head(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `HEAD`."""
    return pipe(ctx, on_method(HEAD))


def on_trace(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `TRACE`."""
    return pipe(ctx, on_method(TRACE))


def on_connect(ctx: context.Context) -> context.StateContext:
    """Continue execution if request method is `CONNECT`."""
    return pipe(ctx, on_method(CONNECT))
