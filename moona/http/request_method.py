from pymon import Future

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPFunc, handler1, skip


@handler1
def method(method: str, nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Handler that matches request method with passed method.

    When methods are equal pipeline is continued, otherwise skipped.

    Args:
        method (str): method to match.
        nxt (HTTPFunc): next func to run.
        ctx (HTTPContext): to match with

    Returns:
        Future[HTTPContext | None]: result.
    """
    match ctx.request_method == method:
        case True:
            return nxt(ctx)
        case False:
            return skip(ctx)


def GET(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with GET method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("GET")(nxt, ctx)


def POST(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with POST method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("POST")(nxt, ctx)


def PATCH(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with PATCH method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("PATCH")(nxt, ctx)


def PUT(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with PUT method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("PUT")(nxt, ctx)


def DELETE(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with DELETE method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("DELETE")(nxt, ctx)


def OPTIONS(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with OPTIONS method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("OPTIONS")(nxt, ctx)


def HEAD(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with HEAD method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("HEAD")(nxt, ctx)


def TRACE(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with TRACE method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("TRACE")(nxt, ctx)


def CONNECT(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:  # noqa
    """Matches request with CONNECT method.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return method("CONNECT")(nxt, ctx)
