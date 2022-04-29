from enum import Enum

from mona.core import HTTPContext
from mona.handlers.core import HTTPHandler, HTTPHandlerResult, http_handler
from mona.handlers.error import HTTPContextError
from mona.monads.result import Failure, Success


class HTTPMethod(Enum):
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
    def _method(ctx: HTTPContext) -> HTTPHandlerResult:
        match ctx.request.method == method_:
            case True:
                return Success(ctx)
            case False:
                return Failure(WrongHTTPMethodError(ctx))

    return _method


def get(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only GET requests."""
    return method(HTTPMethod.GET)


def post(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only POST requests."""
    return method(HTTPMethod.POST)


def patch(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only PATCH requests."""
    return method(HTTPMethod.PATCH)


def put(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only PUT requests."""
    return method(HTTPMethod.PUT)


def delete(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only DELETE requests."""
    return method(HTTPMethod.DELETE)


def options(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only OPTIONS requests."""
    return method(HTTPMethod.OPTIONS)


def head(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only HEAD requests."""
    return method(HTTPMethod.HEAD)


def trace(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only TRACE requests."""
    return method(HTTPMethod.TRACE)


def connect(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that allows only CONNECT requests."""
    return method(HTTPMethod.CONNECT)
