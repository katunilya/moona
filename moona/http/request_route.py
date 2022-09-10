from typing import Callable

from fundom import cmap, future, pipe

from moona.http.context import HTTPContext, get_request_path, get_request_query_string
from moona.http.handlers import HTTPFunc, HTTPHandler, handler, handler1, skip
from moona.utils import decode, str_split


@handler1
def route(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
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
def subroute(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
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
def route_ci(path: str, nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
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
) -> future[HTTPContext | None]:
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


def bind_query(func: Callable[..., HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on path query.

    Args:
        func (Callable[..., HTTPHandler]): to run on request path query.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
        match get_request_query_string(ctx):
            case b"":
                query = {}
            case raw_query:
                query = (
                    pipe(raw_query)
                    << decode("UTF-8")
                    << str_split("&")
                    << cmap(str_split("="))
                    << list
                    << dict
                ).finish()

        handle = func(**query)
        return handle(nxt, ctx)

    return _handler


def bind_params(path: str, func: Callable[..., HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on path params or skips pipeline.

    Args:
        path (str): to match with.
        func (Callable[..., HTTPHandler]): to run on request path params.
    """
    path_parts = path.strip("/").split("/")

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
        request_path_parts = get_request_path(ctx).strip("/").split("/")
        params = ()
        match len(request_path_parts) == len(path_parts):
            case True:
                for part, request_part in zip(path_parts, request_path_parts):
                    match part.startswith("{"), part == request_part:
                        case True, _:
                            params = (*params, request_part)
                        case False, True:
                            continue
                        case False, False:
                            return skip(ctx)
                return func(*params)(nxt, ctx)
            case False:
                return skip(ctx)

    return _handler
