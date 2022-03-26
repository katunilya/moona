from mona import context, state


def parse_headers(ctx: context.Context) -> context.Context:
    """Converts raw request headers into dict[str, str]."""

    if ctx.request_headers is not None:
        return

    ctx.request_headers = dict(
        (key.decode("utf-8").lower(), value.decode("utf-8"))
        for key, value in ctx.raw_headers
    )

    return ctx


def on_header(key: str, value: str) -> context.Handler:
    """Continue execution if request has header `key` of `value`."""

    key = key.lower()

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
