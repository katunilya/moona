from toolz import curried, pipe

from mona import context, handler, state


def has_header(key: str, value: str, required: bool = False) -> handler.Handler:
    """Continue execution if request has header `key` of `value`.

    Accpts only context in RIGHT state. Returns context in RIGHT state if header with
    required value is present in request headers. Returns context in WRONG state if not.

    Args:
        key (str): of header
        value (str): of header

    Returns:
        handler3.Handler: handler
    """
    key = key.lower()
    value = value.encode("UTF-8")

    @state.accepts_right
    def _handler(cnt: context.Context) -> state.State[context.Context]:
        if header := cnt.request.headers.get(key, None):
            return state.right(cnt) if header == value else state.wrong(cnt)

        return state.wrong(cnt)

    return _handler


def take_headers(ctx: context.Context) -> state.State[dict[str, str]]:
    """Extracts request header as dict of strings.

    Args:
        ctx (context.Context): source

    Returns:
        state.State[dict[str, str]]: headers
    """
    return pipe(
        ctx.request.headers,
        curried.valmap(lambda value: value.decode("UTF-8")),
        dict,
        state.right,
    )
