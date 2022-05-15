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


GET = method("GET")
POST = method("POST")
PATCH = method("PATCH")
PUT = method("PUT")
DELETE = method("DELETE")
OPTIONS = method("OPTIONS")
HEAD = method("HEAD")
TRACE = method("TRACE")
CONNECT = method("CONNECT")
