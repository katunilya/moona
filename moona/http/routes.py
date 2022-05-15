from pymon import Future

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPFunc, handler1, skip


@handler1
def route(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Handler that processes ctx only on right path.

    Request path must be exactly the same as path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    match ctx.request_path == path.strip("/"):
        case True:
            return nxt(ctx)
        case False:
            return skip(ctx)


@handler1
def subroute(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Handler that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users".
    """
    path = path.strip("/")
    match ctx.request_path.startswith(path):
        case True:
            ctx.request_path = ctx.request_path.lstrip(path).strip("/")
            return nxt(ctx)
        case False:
            return skip(ctx)


@handler1
def route_ci(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Handler that processes ctx only on right path.

    Request path must be case-insensitive to path passed as an argument to the handler
    HOF. In order to keep them of the same format paths (bth in request and in handler)
    are striped from leading and trailing "/".
    """
    match ctx.request_path.lower() == path.strip("/").lower():
        case True:
            return nxt(ctx)
        case False:
            return skip(ctx)


@handler1
def subroute_ci(
    path: str, nxt: HTTPFunc, ctx: HTTPContext
) -> Future[HTTPContext | None]:
    """Handler that proceeds only when Request path starts with passed path.

    Leading part of the path is removed after processing the request. For example
    request path was "group/users". Subroute waited for "group". After processing this
    handler `HTTPContext` will have "users". Route is case-insensitive.
    """
    path = path.strip("/").lower()
    subroute_len = len(path)
    match ctx.request_path.lower().startswith(path):
        case True:
            ctx.request_path = ctx.request_path[subroute_len:].strip("/")
            return nxt(ctx)
        case False:
            return skip(ctx)
