from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler
from mona.handlers.error import HTTPContextError
from mona.monads.result import Failure, Success


class WrongPathError(HTTPContextError):
    """`HTTPContext` is handled via wrong handler based on path mismatch."""

    def __init__(self, ctx: HTTPContext, path: str) -> None:
        super().__init__(
            ctx,
            f"Wrong path. Requires: {path}. Received: {ctx.request.path}",
            500,
        )


def route(path: str) -> HTTPHandler:
    """`HTTPContext` handler that `Success`fully processes ctx only on right path.

    Request path must be exactly the same as path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    path = path.strip("/")

    @http_handler
    def _route(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.path == path:
            case True:
                return Success(ctx)
            case False:
                return Failure(WrongPathError(ctx, path))

    return _route


def subroute(path: str) -> HTTPHandler:
    """`HTTPHandler` that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users".
    """
    path = path.strip("/")

    @http_handler
    def _subroute(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.path.startswith(path):
            case True:
                ctx.request.path = ctx.request.path.lstrip(path).strip("/")
                return Success(ctx)
            case False:
                return Failure(WrongPathError(ctx, path))

    return _subroute


def ci_route(path: str) -> HTTPHandler:
    """`HTTPContext` handler that `Success`fully processes ctx only on right path.

    Request path must be case-insensitive to path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    path = path.strip("/").lower()

    @http_handler
    def _ci_route(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.path.lower() == path:
            case True:
                return Success(ctx)
            case False:
                return Failure(WrongPathError(ctx, path))

    return _ci_route


def ci_subroute(path: str) -> HTTPHandler:
    """`HTTPHandler` that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users". Route is case-insensitive.
    """
    path = path.strip("/").lower()
    subroute_len = len(path)

    @http_handler
    def _ci_subroute(ctx: HTTPContext) -> HTTPContextResult:
        match ctx.request.path.lower().startswith(path):
            case True:
                ctx.request.path = ctx.request.path[subroute_len:].strip("/")
                return Success(ctx)
            case False:
                return Failure(WrongPathError(ctx, path))

    return _ci_subroute
