from __future__ import annotations

from mona.core import ErrorContext, HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler


class WrongHTTPMethodError(ErrorContext):
    """`HTTPContext` is handled via wrong handler based on method mismatch."""

    def __init__(self, ctx: HTTPContext, method: str) -> None:
        super().__init__(
            ctx,
            f"Wrong HTTP method. Requires: {method}. Received: {ctx.request.method}",
            500,
        )


def method(method_: str) -> HTTPHandler:
    """Continues execution if request method is passed method."""

    @http_handler
    def _method(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.method == method_:
            case True:
                return ctx
            case False:
                return WrongHTTPMethodError(ctx, method_)

    return _method


__GET = method("GET")
__POST = method("POST")
__PATCH = method("PATCH")
__PUT = method("PUT")
__DELETE = method("DELETE")
__OPTIONS = method("OPTIONS")
__HEAD = method("HEAD")
__TRACE = method("TRACE")
__CONNECT = method("CONNECT")


@http_handler
def GET(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on GET method."""
    return __GET(ctx)


@http_handler
def POST(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on POST method."""
    return __POST(ctx)


@http_handler
def PATCH(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on PATCH method."""
    return __PATCH(ctx)


@http_handler
def PUT(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on PUT method."""
    return __PUT(ctx)


@http_handler
def DELETE(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on DELETE method."""
    return __DELETE(ctx)


@http_handler
def OPTIONS(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on OPTIONS method."""
    return __OPTIONS(ctx)


@http_handler
def HEAD(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on HEAD method."""
    return __HEAD(ctx)


@http_handler
def TRACE(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on TRACE method."""
    return __TRACE(ctx)


@http_handler
def CONNECT(ctx: HTTPContext) -> HTTPContextResult:  # noqa
    """`HTTPContext` handler that proceeds `HTTPContext` only on CONNECT method."""
    return __CONNECT(ctx)
