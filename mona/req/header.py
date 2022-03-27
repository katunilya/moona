from toolz import curried
from toolz import functoolz as ft

from mona import context, state


def parse_headers(ctx: context.Context) -> context.Context:
    """Converts raw request headers into dict[str, str]."""
    if ctx.request_headers is not None:
        return

    ctx.request_headers = ft.pipe(
        ctx.raw_headers,
        curried.map(lambda header: (header[0].decode("utf-8").casefold(), header[1])),
        dict,
    )

    return ctx


def on_header(key: str, value: str) -> context.Handler:
    """Continue execution if request has header `key` of `value`."""
    key = key.casefold()
    value = value.encode("utf-8")

    def _handler(ctx: context.Context) -> context.StateContext:
        return (
            state.Valid(ctx)
            if ctx.request_headers.get(key, None) == value
            else state.Invalid(ctx)
        )

    return state.compose(
        parse_headers,
        _handler,
    )
