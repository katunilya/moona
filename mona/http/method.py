from mona.core import ErrorContext
from mona.handlers.core import http_handler
from mona.http.core import HTTPContext, HTTPContextHandler
from mona.monads.pipe import Pipeline


class WrongHTTPMethodError(ErrorContext):
    """`HTTPContext` is handled via wrong handler based on method mismatch."""

    def __init__(self, ctx: HTTPContext, method: str) -> None:
        super().__init__(
            ctx,
            f"Wrong HTTP method. Requires: {method}. Received: {ctx.request_method}",
            500,
        )


def if_method(value: str) -> HTTPContextHandler:
    """Returns `HTTPContext` if its method is same as `value`.

    Args:
        value (str): to compare with.
    """

    @http_handler
    def _handler(ctx: HTTPContext) -> HTTPContext | ErrorContext:
        match ctx.request_method == value:
            case True:
                return ctx
            case False:
                return WrongHTTPMethodError(ctx, value)

    return _handler


def if_get(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is GET."""
    return Pipeline(ctx).then(if_method("GET")).finish()


def if_post(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is POST."""
    return Pipeline(ctx).then(if_method("POST")).finish()


def if_patch(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is PATCH."""
    return Pipeline(ctx).then(if_method("PATCH")).finish()


def if_put(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is PUT."""
    return Pipeline(ctx).then(if_method("PUT")).finish()


def if_delete(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is DELETE."""
    return Pipeline(ctx).then(if_method("DELETE")).finish()


def if_options(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is OPTIONS."""
    return Pipeline(ctx).then(if_method("OPTIONS")).finish()


def if_head(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is HEAD."""
    return Pipeline(ctx).then(if_method("HEAD")).finish()


def if_trace(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is TRACE."""
    return Pipeline(ctx).then(if_method("TRACE")).finish()


def if_connect(ctx: HTTPContext) -> HTTPContext | ErrorContext:
    """Returns `HTTPContext` if its method is CONNECT."""
    return Pipeline(ctx).then(if_method("CONNECT")).finish()
