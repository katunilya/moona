from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, TypeVar

from pymon.core import hof_2, hof_3
from toolz import keymap

from moona.context import BaseContext, Receive, Scope, Send

T = TypeVar("T")

ClientInfo = NamedTuple("ClientInfo", [("host", str), ("port", int)])
ServerInfo = NamedTuple("ServerInfo", [("host", str), ("port", int | None)])


@dataclass(slots=True)
class HTTPContext(BaseContext):
    """Object that contains entire information related to HTTP Request.

    Mostly it's structure is replication of HTTP Connection Scope of ASGI Specification.
    It contains information on both request and response and also functions for sending
    and receiving information.

    Note:
        https://asgi.readthedocs.io/en/latest/specs/www.html#
    """

    # common scope data
    scope_type: str
    asgi_version: str
    asgi_spec_version: str
    http_version: str
    scheme: str
    server: ServerInfo
    client: ClientInfo

    # request info
    request_method: str
    request_path: str
    request_headers: dict[bytes, bytes]
    request_body: bytes
    request_query_string: bytes

    # response info
    response_status: int
    response_body: bytes | None
    response_headers: dict[bytes, bytes]

    # context state
    received: bool
    started: bool
    closed: bool

    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.scope_type = scope["type"]
        self.asgi_version = scope["asgi"]["version"]
        self.asgi_spec_version = scope["asgi"].get("spec_version", "2.0")
        self.http_version = scope.get("http_version", "1.1")
        self.scheme = scope.get("http_version", "http")
        self.client = ClientInfo(scope["client"][0], scope["client"][1])
        self.server = ServerInfo(scope["server"][0], scope["server"][1])

        self.receive = receive
        self.send = send

        self.request_method = scope["method"]
        self.request_path = scope["path"].strip("/")
        self.request_query_string = scope["query_string"]
        self.request_headers = keymap(bytes.lower, dict(scope.get("headers", [])))
        self.request_body = b""

        self.response_body = None
        self.response_headers = {}
        self.response_status = 200

        self.received = False
        self.started = False
        self.closed = False


# funcs
@hof_2
def set_response_body(data: bytes, ctx: HTTPContext) -> HTTPContext:
    """Set response body.

    Response body is some byte string so default `HTTPFunc` accepts `bytes`.

    Args:
        data (bytes): body to set.
        ctx (HTTPContext): context to set body to.
    """
    ctx.response_body = data
    return ctx


@hof_2
def set_response_status(code: int, ctx: HTTPContext) -> HTTPContext:
    """Set response status code.

    Args:
        code (int): status code to set.
        ctx (HTTPContext): context to set status code to.
    """
    ctx.response_status = code
    return ctx


@hof_3
def set_response_header(name: str, value: str, ctx: HTTPContext) -> HTTPContext:
    """Set `value` for response header `name`.

    Args:
        name (str): header name.
        value (str): header value.
        ctx (HTTPContext): to set header to.
    """
    _name = name.encode("UTF-8").lower()
    _value = value.encode("UTF-8")
    ctx.response_headers[_name] = _value
    return ctx


@hof_2
def set_received(value: bool, ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `received` to `value`."""
    ctx.received = value
    return ctx


@hof_2
def set_started(value: bool, ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `started` to `value`."""
    ctx.started = value
    return ctx


@hof_2
def set_closed(value: bool, ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `closed` to `value`."""
    ctx.closed = value
    return ctx
