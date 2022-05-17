from logging.handlers import HTTPHandler

from pymon import Future

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPFunc, handler, skip


def has_header(name: str) -> HTTPHandler:
    """Processes next `HTTPFunc` only when request has passed header.

    Args:
        name (str): to check for.
    """
    raw_name = name.encode("UTF-8").lower()

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        match ctx.request_headers.get(raw_name, None):
            case None:
                return skip(ctx)
            case _:
                return nxt(ctx)

    return _handler


def matches_header(name: str, value: str) -> HTTPHandler:
    """Processes next `HTTPFunc` only when request has valid headers.

    Args:
        name (str): to check header.
        value (str): to check. Optional. If not passed, than presence of header is
        checked.
    """
    raw_name = name.encode("UTF-8").lower()
    raw_value = value.encode("UTF-8")

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        match ctx.request_headers.get(raw_name, None) == raw_value:
            case True:
                return nxt(ctx)
            case False:
                return skip(ctx)

    return _handler
