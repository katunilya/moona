from enum import Enum

from mona.core import HTTPContext, HTTPContextError
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler


class HTTPMethod(Enum):
    """HTTP Method values based on RFC 2616.

    Note:
        * https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.1.1
    """

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    TRACE = "TRACE"
    CONNECT = "CONNECT"


class WrongHTTPMethodError(HTTPContextError):
    """`HTTPContext` is handled via wrong handler based on method mismatch."""

    def __init__(self, ctx: HTTPContext, method: str) -> None:
        super().__init__(
            ctx,
            f"Wrong HTTP method. Requires: {method}. Received: {ctx.request.method}",
            500,
        )


def method(method_: HTTPMethod) -> HTTPHandler:
    """Continues execution if request method is passed method."""

    @http_handler
    def _method(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.method == method_:
            case True:
                return ctx
            case False:
                return WrongHTTPMethodError(ctx)

    return _method


GET = method(HTTPMethod.GET)
POST = method(HTTPMethod.POST)
PATCH = method(HTTPMethod.PATCH)
PUT = method(HTTPMethod.PUT)
DELETE = method(HTTPMethod.DELETE)
OPTIONS = method(HTTPMethod.OPTIONS)
HEAD = method(HTTPMethod.HEAD)
TRACE = method(HTTPMethod.TRACE)
CONNECT = method(HTTPMethod.CONNECT)
