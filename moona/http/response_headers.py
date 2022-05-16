from pymon import Future, Pipe

from moona.http.context import HTTPContext, set_response_header
from moona.http.handlers import HTTPFunc, handler2


@handler2
def header(
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


def content_type(value: str):
    """`HTTPHandler` that sets "Content-Type" response header.

    Args:
        value (str): of header.

    Returns:
        HTTPHandler: handler.
    """
    return header("content-type", value)


def content_type_application_json(
    nxt: HTTPFunc, ctx: HTTPContext
) -> Future[HTTPContext | None]:
    """Sets "Content-Type: application/json" response header.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.

    Returns:
        Future[HTTPContext | None]: result
    """
    return content_type("application/json")(nxt, ctx)


def content_type_text_plain(
    nxt: HTTPFunc, ctx: HTTPContext
) -> Future[HTTPContext | None]:
    """Sets "Content-Type: text/plain" response header.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process

    Returns:
        Future[HTTPContext | None]: result.
    """
    return content_type("text/plain")(nxt, ctx)
