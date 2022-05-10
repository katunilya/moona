from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Awaitable, Callable, NamedTuple, TypeVar

from toolz import keymap

from mona.core import BaseContext, ErrorContext, Message, Receive, Scope, Send
from mona.monads.future import Future

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

    # event functions
    __receive: Receive
    __send: Send

    # request info
    request_method: str
    request_path: str
    request_headers: dict[bytes, bytes]
    request_body: bytes | None
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

        self.__receive = receive
        self.__send = send

        self.request_method = scope["method"]
        self.request_path = scope["path"].strip("/")
        self.request_query_string = scope["query_string"]
        self.request_headers = keymap(bytes.lower, dict(scope.get("headers", [])))
        self.request_body = None

        self.response_body = None
        self.response_headers = {}
        self.response_status = 200

        self.received = False
        self.started = False
        self.closed = False


# decorators
def handler(func: Callable[[HTTPContext], T]) -> Callable[[HTTPContext], T]:
    """Decorator that protects sync function from non-`HTTPContext` args."""

    @wraps(func)
    def _wrapper(ctx: HTTPContext) -> T:
        match ctx:
            case HTTPContext():
                return func(ctx)
            case other:
                return other

    return _wrapper


def async_handler(
    func: Callable[[HTTPContext], Awaitable[T]]
) -> Callable[[HTTPContext], Future[T]]:
    """Decorator that protects async function from from non-`HTTPContext` args."""

    @wraps(func)
    def _wrapper(ctx: HTTPContext) -> Future[T]:
        match ctx:
            case HTTPContext():
                return Future(func(ctx))
            case other:
                return Future.identity(other)

    return _wrapper


# event handlers
def send_async(msg: Message) -> Callable[[HTTPContext], Future[HTTPContext]]:
    """Asynchronously send passed `Message` to client.

    Args:
        msg (Message): to send.
    """

    @async_handler
    async def _send_async(ctx: HTTPContext) -> HTTPContext:
        await ctx.__send(msg)
        return ctx

    return _send_async


def receive_async(ctx: HTTPContext) -> Future[Message]:
    """Asynchronously receive `Message` from client.

    Returns:
        Future[Message]: received.
    """
    return Future(ctx.__receive())


# setters
@handler
def set_received_true(ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `received` to `True`."""
    ctx.received = True
    return ctx


@handler
def set_started_true(ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `started` to `True`."""
    ctx.started = True
    return ctx


@handler
def set_closed_true(ctx: HTTPContext) -> HTTPContext:
    """Sync `HTTPContext` that sets `closed` to `True`."""
    ctx.closed = True
    return ctx


# getters
@handler
def get_scope_type(ctx: HTTPContext):
    """Returns `scope_type`."""
    return ctx.scope_type


@handler
def get_asgi_version(ctx: HTTPContext):
    """Returns `asgi_version`."""
    return ctx.asgi_version


@handler
def get_asgi_spec_version(ctx: HTTPContext):
    """Returns `asgi_spec_version`."""
    return ctx.asgi_spec_version


@handler
def get_http_version(ctx: HTTPContext):
    """Returns `http_version`."""
    return ctx.http_version


@handler
def get_scheme(ctx: HTTPContext):
    """Returns `scheme`."""
    return ctx.scheme


@handler
def get_client(ctx: HTTPContext):
    """Returns `client`."""
    return ctx.client


@handler
def get_server(ctx: HTTPContext):
    """Returns `server`."""
    return ctx.server


@handler
def get_request_method(ctx: HTTPContext):
    """Returns `request_method`."""
    return ctx.request_method


@handler
def get_request_path(ctx: HTTPContext):
    """Returns `request_path`."""
    return ctx.request_path


@handler
def get_request_query_string(ctx: HTTPContext):
    """Returns `request_query_string`."""
    return ctx.request_query_string


@handler
def get_request_headers(ctx: HTTPContext):
    """Returns `request_headers`."""
    return ctx.request_headers


@handler
def get_request_body(ctx: HTTPContext):
    """Returns `request_body`."""
    return ctx.request_body


@handler
def get_response_body(ctx: HTTPContext):
    """Returns `response_body`."""
    return ctx.response_body


@handler
def get_response_headers(ctx: HTTPContext):
    """Returns `response_headers`."""
    return ctx.response_headers


@handler
def get_response_status(ctx: HTTPContext):
    """Returns `response_status`."""
    return ctx.response_status


@handler
def get_received(ctx: HTTPContext):
    """Returns `received`."""
    return ctx.received


@handler
def get_started(ctx: HTTPContext):
    """Returns `started`."""
    return ctx.started


@handler
def get_closed(ctx: HTTPContext):
    """Returns `closed`."""
    return ctx.closed


HTTPContextHandler = Callable[[HTTPContext], HTTPContext | ErrorContext]
AsyncHTTPContextHandler = Callable[[HTTPContext], Awaitable[HTTPContext | ErrorContext]]
