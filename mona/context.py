import dataclasses
import typing

import toolz

from mona import state

Message = dict[str, typing.Any]
Scope = Message
Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]
ASGIServer = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]


@dataclasses.dataclass
class Client:
    """Information about request client."""

    __slots__ = "host", "port"
    host: str
    port: int


@dataclasses.dataclass
class Server:
    """Information about server excepted request."""

    __slots__ = "host", "port"
    host: str
    port: typing.Optional[int]


@dataclasses.dataclass
class Request:
    """Immutable request data."""

    __slots__ = (
        "type_",
        "method",
        "subprotocols",
        "asgi_version",
        "asgi_spec_version",
        "http_version",
        "scheme",
        "path",
        "query_string",
        "headers",
        "body",
        "server",
        "client",
    )

    type_: str
    method: typing.Optional[str]
    subprotocols: typing.Optional[typing.Iterable[str]]
    asgi_version: str
    asgi_spec_version: str
    http_version: str
    scheme: str
    path: str
    query_string: typing.ByteString
    headers: dict[str, typing.ByteString]
    body: typing.Optional[typing.ByteString]
    server: Server
    client: Client


def __request_from_scope(scope: Scope) -> Request:
    method, subprotocols = (
        (scope["method"], None)
        if scope["type"] == "http"
        else (None, scope["subprotocols"])
    )
    headers = toolz.keymap(
        lambda key: key.decode("UTF-8").lower(),
        dict(header for header in scope["headers"]),
    )
    return Request(
        type_=scope["type"],
        method=method,
        subprotocols=subprotocols,
        asgi_version=scope["asgi"]["version"],
        asgi_spec_version=scope["asgi"]["spec_version"],
        http_version=scope["http_version"],
        scheme=scope["scheme"],
        path=scope["path"].strip("/"),
        query_string=scope["query_string"],
        headers=headers,
        body=None,
        client=Client(host=scope["client"][0], port=scope["client"][1]),
        server=Server(host=scope["server"][0], port=scope["server"][1]),
    )


def __request_copy(request: Request) -> Request:
    return Request(
        type_=request.type_,
        method=request.method,
        subprotocols=request.subprotocols,
        asgi_version=request.asgi_version,
        asgi_spec_version=request.asgi_spec_version,
        http_version=request.http_version,
        scheme=request.scheme,
        path=request.path,
        query_string=request.query_string,
        headers=request.headers,
        body=request.body,
        client=request.client,
        server=request.server,
    )


@dataclasses.dataclass
class Response:
    """Request response data."""

    __slots__ = ("body", "headers", "status")
    body: typing.Any
    headers: dict[typing.ByteString, typing.ByteString]
    status: int


def __empty_response() -> Response:
    return Response(None, {}, 200)


def __response_copy(response: Response) -> Response:
    return Response(
        body=response.body,
        headers=response.headers,
        status=response.status,
    )


@dataclasses.dataclass
class Context:
    """Wrapper for request data processing."""

    request: Request
    response: Response
    receive: Receive
    send: Send
    error: typing.Optional[BaseException] = None


def from_asgi(scope: Scope, receive: Receive, send: Send) -> Context:
    """Create context from ASGI function args.

    Args:
        scope (Scope): ASGI scope
        receive (Receive): ASGI receive
        send (Send): ASGI send

    Returns:
        Context: for storing info about request
    """
    return Context(
        __request_from_scope(scope),
        __empty_response(),
        receive,
        send,
    )


def copy(ctx: Context) -> Context:
    """Create `Context` from another `Context` as a copy.

    Args:
        context (Context): to copy

    Returns:
        Context: copy
    """
    return Context(
        __request_copy(ctx.request),
        __response_copy(ctx.response),
        ctx.receive,
        ctx.send,
        ctx.error,
    )


StateContext = state.State[Context]
