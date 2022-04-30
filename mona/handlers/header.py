from typing import Callable

from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler
from mona.monads.maybe import Maybe, Nothing, Some
from mona.monads.result import Success


def set_header(name: str, value: str) -> HTTPHandler:
    """`HTTPHandler` that sets new response header based on passed values.

    Response header name is lowercased despite headers are case-insensitive based on
    RFC 2616. Also header name and value are converted to `bytes` as `Context` stores
    response headers as `dict[bytes, bytes]` based on ASGI specification.

    Specifications
    * RFC 2616 - 4.2 Message Headers -
        https://datatracker.ietf.org/doc/html/rfc2616#section-4.2
    * ASGI Specification - Response start event -
        https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event

    Args:
        name (str): header name.
        value (str): header value.

    Returns:
        HTTPHandler: actually performs settings response header.
    """
    name: bytes = name.lower().decode("UTF-8")
    value: bytes = value.decode("UTF-8")

    @http_handler
    def _handler(ctx: HTTPContext) -> HTTPContextResult:
        ctx.response.headers[name] = value
        return Success(ctx)

    return _handler


def remove_header(name: str) -> HTTPHandler:
    """`HTTPHandler` that removes response header based on passed header name.

    Header name can be passed in any case as based on RFC 2616 headers are
    case-insensitive. Due to this and based on ASGI specification response headers are
    stored as `dict[bytes, bytes]` where key is lowercase byte string. Passed `name` is
    converted to lowercase, than to `bytes` and than key is removed from response
    headers `dict`.

    Specifications
    * RFC 2616 - 4.2 Message Headers -
        https://datatracker.ietf.org/doc/html/rfc2616#section-4.2
    * ASGI Specification - Response start event -
        https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event


    Args:
        name (str): header name to remove.

    Returns:
        HTTPHandler: actually performs remove of response header.
    """
    name: bytes = name.lower().decode("UTF-8")

    @http_handler
    def _handler(ctx: HTTPContext) -> HTTPContextResult:
        del ctx.response.headers[name]
        return Success(ctx)

    return _handler


def get_header(
    name: str,
) -> Callable[[HTTPContext], Maybe[tuple[str, str]]]:
    """Try to get concrete `HTTPRequest` header by name.

    If `name` is present in dictionary of headers than `Some` header is returned.
    Otherwise `Nothing`.

    Args:
        name (str): name of the header to try to get.

    Returns:
        Callable[[HTTPContext], Maybe[tuple[str, str]]]: function that actually returns
        headers.
    """
    name: str = name.lower()

    def _getter(ctx: HTTPContext) -> Maybe[tuple[str, str]]:
        match ctx.request.headers.get(name, None):
            case None:
                return Nothing()
            case value:
                return Some((name, value))

    return _getter


def get_headers(ctx: HTTPContext) -> Maybe[dict[str, str]]:
    """Try to get all `HTTPRequest` headers.

    If `HTTPRequest` headers are empty dictionary than `Nothing` is returned. Otherwise
    `Some` headers.

    Args:
        ctx (HTTPContext): to get headers from.

    Returns:
        Maybe[dict[str, str]]: `None`-safe `HTTPRequest` headers.
    """
    match ctx.request.headers:
        case {}:
            return Nothing()
        case headers:
            return Some(headers)
