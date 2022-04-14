from mona import context, handler, state


def on_route(pattern: str) -> handler.Handler:
    """If request `path` is the same as `pattern` than context is valid."""
    pattern = pattern.strip("/")

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        return state.right(ctx) if pattern == ctx.request.path else state.wrong(ctx)

    return _handler


def on_subroute(pattern: str) -> handler.Handler:
    """Returns valid context without subroute part of it if `pattern` equals `path`."""
    pattern = pattern.strip("/")

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        if ctx.request.path.startswith(pattern):
            subroute = len(pattern)
            ctx.request.path = ctx.request.path[subroute:].strip("/")
            return state.right(ctx)

        return state.wrong(ctx)

    return _handler


def on_ciroute(pattern: str) -> handler.Handler:
    """Case insensitive version of `on_route`."""
    pattern = pattern.strip("/").lower()

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        return (
            state.right(ctx)
            if ctx.request.path.lower() == pattern
            else state.wrong(ctx)
        )

    return _handler


def on_cisubroute(pattern: str) -> handler.Handler:
    """Case insensitive version of `on_subroute`."""
    pattern = pattern.strip("/").lower()

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        if ctx.request.path.lower().startswith(pattern):
            subroute_len = len(pattern)
            ctx.request.path = ctx.request.path[subroute_len:].strip("/")
            return state.right(ctx)
        return state.wrong(ctx)

    return _handler
