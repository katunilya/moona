import toolz

from mona.http.core import HTTPContext, HTTPContextHandler, get_response_body, handler
from mona.monads.maybe import Maybe
from mona.monads.pipe import Pipe
from mona.utils import decode_utf_8, encode_utf_8


def convert_header_to_str(header: tuple[bytes, bytes]) -> tuple[str, str]:  # noqa
    return decode_utf_8(header[0]), decode_utf_8(header[1])


def convert_headers_to_str(headers: dict[bytes, bytes]) -> dict[str, str]:  # noqa
    return toolz.itemmap(convert_header_to_str, headers)


def set_header(name: str, value: str) -> HTTPContextHandler:
    """Sets passed (name, value) pairs to Response Headers.

    Header name lowercased. Both name and value are converted to byte strings. There is
    only method called `set_header` which sets header for response, as it doesn't make
    matter if one changes request headers.

    Args:
        name (str): of header.
        value (str): of header.
    """
    bytes_name = encode_utf_8(name).lower()
    bytes_value = encode_utf_8(value)

    @handler
    def _handler(ctx: HTTPContext) -> HTTPContext:
        ctx.response_headers[bytes_name] = bytes_value
        return ctx

    return _handler


def set_content_type(value: str) -> HTTPContextHandler:
    """Sets "Content-Type" response header.

    Args:
        value (str): of "Content-Type" response header.
    """
    return set_header("content-type", value)


def set_content_type_text(ctx: HTTPContext) -> HTTPContext:
    """Sets "Content-Type" header to "text/plain"."""
    return Pipe(ctx).then(set_content_type("text/plain"))


def set_content_type_json(ctx: HTTPContext) -> HTTPContext:
    """Sets "Content-Type" header to "application/json"."""
    return Pipe(ctx).then(set_content_type("application/json"))


def set_content_length(value: int | None = None) -> HTTPContext:
    """Sets "Content-Length" response header.

    Args:
        value (int): if "Content-Length" response header.
    """

    @handler
    def _handler(ctx: HTTPContext) -> HTTPContext:
        ctx.response_headers[b"content-type"] = (
            Maybe.unit(value)
            .then(Maybe.returns(str))
            .then(Maybe.returns(encode_utf_8))
            .otherwise_replace(
                Pipe(ctx)
                .then(get_response_body)
                .then_maybe(Maybe.unit)
                .then(Maybe.returns(len))
                .then(Maybe.returns(str))
                .then(Maybe.returns(encode_utf_8))
                .otherwise_replace(b"0")
                .value
            )
            .value
        )
        return ctx

    return _handler
