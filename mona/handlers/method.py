from __future__ import annotations

from mona.core import HTTPContext, HTTPContextError
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler


class WrongHTTPMethodError(HTTPContextError):
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


GET = method("GET")
POST = method("POST")
PATCH = method("PATCH")
PUT = method("PUT")
DELETE = method("DELETE")
OPTIONS = method("OPTIONS")
HEAD = method("HEAD")
TRACE = method("TRACE")
CONNECT = method("CONNECT")
