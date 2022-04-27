from dataclasses import dataclass
from functools import reduce
from typing import Any, Awaitable, Callable

from mona.monads import future
from mona.monads.result import Result, Success
from mona.utils import decode_headers

Message = dict[str, Any]
Scope = Message
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
ASGIData = tuple[Scope, Receive, Send]
Header = tuple[str, str]
Headers = dict[str, str]


@dataclass
class ClientInfo:
    """Information related to client that send the request.

    Based on ASGI specification client in HTTP and Websocket connection scope is a pair
    of host and port where host is IPv4 or IPv6 address or unix socketand port is remote
    port integer. Port is optional.

    Note:
        Websockets are not supported.
    """

    host: str
    port: int | None = None


@dataclass
class ServerInfo:
    """Information related to server that received the request.

    Based on ASGI specification server in HTTP and Websocket connection scope is a pair
    of host and port where host is the listening address or unix socket for this server
    and port is the interger listening port. Port is optional.

    Note:
        Websockets are not supported.
    """

    host: str
    port: int | None = None


@dataclass
class HTTPRequest:
    """Information related to HTTP request from ASGI Connection Scope object.

    Object that contains information related to HTTP Request based on ASGI
    specification.

    Note:
        https://asgi.readthedocs.io/en/latest/specs/www.html#

    Attributes:
        type_ (str): "http" or "websocket" string which specifies kind of request.
        method (str): HTTP method name, uppercased.
        asgi_version (str): version of the ASGI spec.
        asgi_spec_version (str): version of the ASGI HTTP spec this server understands;
        one of "2.0", "2.1", "2.2" or "2.3". Optional; if missing assume "2.0".
        http_version (str): one of "1.1" or "2". Optional; if missing default is "1.1".
        scheme (str): URL scheme portion (likely "http" or "https"). Optional (but must
        not be empty); Defaults to "http".
        path (str): HTTP request target excluding any query string, with percent-encoded
        sequences and UTF-8 byte sequences decoded into characters.
        query_string (bytes): URL portion after the ?, percent-encoded.
        headers (dict[str, str]): dictionary for request headers.
        body (bytes | None): request body. `None` by default.
        server (ServerInfo): information about server received request.
        client (ClientInfo): information about client sent the request.
    """

    __slots__ = (
        "type_",
        "method",
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
    method: str
    asgi_version: str
    asgi_spec_version: str
    http_version: str
    scheme: str
    path: str
    query_string: bytes
    headers: dict[str, str]
    body: bytes | None
    server: ServerInfo
    client: ClientInfo


def __create_http_request(scope: Scope) -> HTTPRequest:
    type_ = scope["type"]
    asgi_version = scope["asgi"]["version"]
    method = scope["method"]
    asgi_spec_version = scope["asgi"].get("spec_version", "2.0")
    http_version = scope.get("http_version", "1.1")
    scheme = scope.get("http_version", "http" if type_ == "http" else "ws")
    path = scope["path"].strip("/")
    query_string = scope["query_string"]
    client = ClientInfo(scope["client"]["host"], scope["client"]["port"])
    server = ServerInfo(scope["server"]["host"], scope["server"]["port"])
    headers = decode_headers(scope.get("headers", []))
    body = None
    return HTTPRequest(
        type_,
        method,
        asgi_version,
        asgi_spec_version,
        http_version,
        scheme,
        path,
        query_string,
        headers,
        body,
        server,
        client,
    )


def __copy_http_request(request: HTTPRequest) -> HTTPRequest:
    return HTTPRequest(
        request.type_,
        request.method,
        request.asgi_version,
        request.asgi_spec_version,
        request.http_version,
        request.scheme,
        request.path,
        request.query_string,
        request.headers,
        request.body,
        request.client,
        request.server,
    )


@dataclass
class HTTPResponse:
    """Information related to HTTP Response sent by the application.

    Response contains both information for Response Start send event and Response Body
    send event.

    Attributes:
        status (int): response status code. Defaults to 200 (SUCCESS).
        headers (dict[str, str]): dictionary of response headers. Defaults to dict().
        body (bytes | None): response body. Defaults to b''.
    """

    __slots__ = (
        "status",
        "headers",
        "body",
    )
    status: int = 200
    headers: dict[str, str] = {}
    body: bytes = b""


def __copy_http_response(response: HTTPResponse) -> HTTPResponse:
    return HTTPResponse(
        response.status,
        response.headers,
        response.body,
    )


@dataclass
class HTTPContext:
    """Object that contains entire information related to HTTP Request.

    Mostly it's structure is replication of HTTP Connection Scope of ASGI Specification.
    It contains information on both request and response and also functions for sending
    and receiving information.

    Note:
        https://asgi.readthedocs.io/en/latest/specs/www.html#

    Attributes:
        request (HTTPRequest): information received by the server. response
        (HTTPResponse): information that should be sent by the server.
        receive (Receive): function for acquiring events from client. send (Send):
        function for sending events to the client.
        started (bool): flag that defines if response has started.
        closed (bool): flag that defines if connection is closed due to Timeout from
        user or request finish.
    """

    request: HTTPRequest
    response: HTTPResponse
    receive: Receive
    send: Send
    started: bool = False
    closed: bool = False


def create_http_context(scope: Scope, receive: Receive, send: Send) -> HTTPContext:
    """Create context from ASGI function args.

    Args:
        scope (Scope): ASGI scope.
        receive (Receive): ASGI receive.
        send (Send): ASGI send.

    Returns:
        HTTPContext: for storing info about request
    """
    return HTTPContext(
        request=__create_http_request(scope),
        response=HTTPResponse(),
        receive=receive,
        send=send,
    )


def copy_http_context(ctx: HTTPContext) -> HTTPContext:
    """Create complete copy of HTTPContext.

    This function is needed to avoid side effects due to reference nature of Python when
    using `choose` combinator.

    Args:
        ctx (HTTPContext): to be copied.

    Returns:
        HTTPContext: copy.
    """
    return HTTPContext(
        request=__copy_http_request(ctx.request),
        response=__copy_http_response(ctx.response),
        receive=ctx.receive,
        send=ctx.send,
        started=ctx.started,
        closed=ctx.closed,
    )


HTTPContextResult = Result[HTTPContext, Exception]
HTTPContextHandler = Callable[
    [HTTPContextResult], HTTPContextResult | Awaitable[HTTPContextResult]
]


def handler(
    func: Callable[[HTTPContext], HTTPContextResult | Awaitable[HTTPContextResult]]
) -> HTTPContextHandler:
    """Mandatory decorator for `HTTPContextHandler`.

    This decorator provides `Result` monad handling logic for `HTTPContextHandler` out
    of the box. With it you don't need to explicitly mention that handler excepts only
    `Success` `HTTPContext`. In other words it transforms function that accepts
    `HTTPContext` to function that accepts `Result[Context, Exception]` and will be
    processed only when one is `Success[Context]`. Another requirement for `HTTPContext`
    is that it must not be closed to be processed next.

    Example::

            @handler
            def h(ctx: Context) -> Result[Context]:
               ...

            h(Success(ctx))  # executed
            h(Failure(None))  # not executed

    Args:
        func (Callable[[HTTPContext], HTTPContextResult |
        Awaitable[HTTPContextResult]]]): to be decorated

    Returns:
        HTTPContextHandler: ready-to-use HTTP Context Handler
    """

    def _func(ctx: HTTPContextResult) -> HTTPContextResult:
        match ctx:
            case Success(HTTPContext(closed=False)):
                return ctx >> func
            case other:
                return other

    return _func


def __next_on_some(
    current_func: HTTPContextHandler, next_func: HTTPContextHandler
) -> HTTPContextHandler:
    @handler
    async def _func(ctx: HTTPContext) -> HTTPContextResult:
        match await (
            future.from_value(ctx) >> copy_http_context >> Success >> current_func
        ):
            case Success() as success:
                return success
            case _:
                return await (future.from_value(ctx) >> Success >> next_func)

    return _func


def choose(*funcs: HTTPContextHandler) -> HTTPContextHandler:
    """Logical combinator of `HTTPContextHandler`s catching first `Success` result.

    Sequentially executes passed `HTTPContextHandler`s till one of them returns
    `HTTPContextResult` which would be returned right away.

    In case `func` is empty iterable `future.identity` function is returns so `choose`
    won't critically affect application behavior.

    Example::

            c = choose(
                func_1,  # returns Failure
                func_2,  # returns Success
                func_3,  # returns Success
            )

            result = await (future.from_value(ctx) >> c)  # result of func_2

    Returns:
        HTTPContextHandler: composed function
    """
    match funcs:
        case ():
            return future.identity
        case _:
            return reduce(__next_on_some, funcs)
