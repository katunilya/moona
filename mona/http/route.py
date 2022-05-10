from mona.core import ErrorContext
from mona.http.core import HTTPContext, HTTPContextHandler, handler


class WrongRouteError(ErrorContext):
    """`HTTPContext` is handled via wrong handler based on path mismatch."""

    def __init__(self, ctx: HTTPContext, path: str) -> None:
        super().__init__(
            ctx,
            f"Wrong path. Requires: {path}. Received: {ctx.request_path}",
            500,
        )


def if_route(path: str) -> HTTPContextHandler:
    """Handler that processes ctx only on right path.

    Request path must be exactly the same as path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    path = path.strip("/")

    @handler
    def _handler(ctx: HTTPContext) -> HTTPContext | ErrorContext:
        match ctx.request_path == path:
            case True:
                return ctx
            case False:
                return WrongRouteError(ctx, path)

    return _handler


def if_subroute(path: str) -> HTTPContextHandler:
    """Handler that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users".
    """
    path = path.strip("/")

    @handler
    def _subroute(ctx: HTTPContext) -> HTTPContext | ErrorContext:
        match ctx.request_path.startswith(path):
            case True:
                ctx.request_path = ctx.request_path.lstrip(path).strip("/")
                return ctx
            case False:
                return WrongRouteError(ctx, path)

    return _subroute


def if_ci_route(path: str) -> HTTPContextHandler:
    """Handler that processes ctx only on right path.

    Request path must be case-insensitive to path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    path = path.strip("/").lower()

    @handler
    def _ci_route(ctx: HTTPContext) -> HTTPContext | ErrorContext:
        match ctx.request_path.lower() == path:
            case True:
                return ctx
            case False:
                return WrongRouteError(ctx, path)

    return _ci_route


def if_ci_subroute(path: str) -> HTTPContextHandler:
    """Handler that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users". Route is case-insensitive.
    """
    path = path.strip("/").lower()
    subroute_len = len(path)

    @handler
    def _ci_subroute(ctx: HTTPContext) -> HTTPContext | ErrorContext:
        match ctx.request_path.lower().startswith(path):
            case True:
                ctx.request_path = ctx.request_path[subroute_len:].strip("/")
                return ctx
            case False:
                return WrongRouteError(ctx, path)

    return _ci_subroute
