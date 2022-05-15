from pymon import Future, Pipe

from moona.http.context import HTTPContext, set_response_header
from moona.http.handlers import HTTPFunc, HTTPHandler, handler2


@handler2
def set_header(
    name: str,
    value: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
    """`HTTPHandler` that sets response header.

    Args:
        name (str): of header.
        value (str): of header.
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.

    Returns:
        Future[HTTPContext | None]: result.
    """
    return Pipe(ctx) << set_response_header(name, value) >> nxt


def set_content_type(value: str) -> HTTPHandler:
    """`HTTPHandler` that sets "Content-Type" response header.

    Args:
        value (str): of header.

    Returns:
        HTTPHandler: handler.
    """
    return set_header("Content-Type", value)
