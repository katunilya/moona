from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from toolz import keymap

from mona.monads.core import Bindable

Message = dict[str, Any]
Scope = Message
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
ASGIData = tuple[Scope, Receive, Send]


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
    headers: dict[bytes, bytes]
    body: bytes | None
    server: ServerInfo
    client: ClientInfo

    @staticmethod
    def create(scope: Scope) -> "HTTPRequest":
        """Create `HTTPRequest` object from ASGI scope.

        Args:
            scope (Scope): ASGI scope.

        Returns:
            HTTPRequest: result.
        """
        type_ = scope["type"]
        asgi_version = scope["asgi"]["version"]
        method = scope["method"]
        asgi_spec_version = scope["asgi"].get("spec_version", "2.0")
        http_version = scope.get("http_version", "1.1")
        scheme = scope.get("http_version", "http" if type_ == "http" else "ws")
        path = scope["path"].strip("/")
        query_string = scope["query_string"]
        client = ClientInfo(scope["client"][0], scope["client"][1])
        server = ServerInfo(scope["server"][0], scope["server"][1])
        headers = keymap(bytes.lower, dict(scope.get("headers", [])))
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

    def copy(self: "HTTPRequest") -> "HTTPRequest":
        """Create a deepcopy of `HTTPRequest`.

        Returns:
            HTTPRequest: deepcopy.
        """
        return HTTPRequest(
            self.type_,
            self.method,
            self.asgi_version,
            self.asgi_spec_version,
            self.http_version,
            self.scheme,
            self.path,
            self.query_string,
            self.headers.copy(),
            self.body,
            self.client,
            self.server,
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
    status: int
    headers: dict[str, str]
    body: bytes

    @staticmethod
    def empty() -> "HTTPResponse":
        """Create empty `HTTPResponse`.

        Empty `HTTPResponse` has 200 OK status code, empty dictionary for headers and
        empty bytes string for body.

        Returns:
            HTTPResponse: empty response.
        """
        return HTTPResponse(
            status=200,
            headers={},
            body=b"",
        )

    def copy(self: "HTTPResponse") -> "HTTPResponse":
        """Create a deepcopy of `HTTPResponse`.

        Returns:
            HTTPResponse: deepcopy of HTTPResponse.
        """
        return HTTPResponse(
            self.status,
            self.headers.copy(),
            self.body,
        )


class BaseContext(ABC, Bindable):
    """Base class for each kind of Context handled by application.

    Mainly there are 3 kinds:
    * `HTTPContext` (implemented)
    * `LifespanContext` (in progress)
    * `WebsocketContext` (not implemented)
    """

    def __rshift__(
        self,
        handler: Callable[[BaseContext | ContextError], BaseContext | ContextError],
    ) -> BaseContext | ContextError:
        """Binding for `BaseContext`.

        This must be used only for sync handler for easier to read syntax. For async
        functions use `Future`.

        Args:
            handler (Callable[[BaseContext | ContextError], BaseContext |
            ContextError]): sync handler to execute with this ctx.

        Returns:
            BaseContext | ContextError: result of handler.
        """
        return handler(self)


@dataclass
class LifespanContext(BaseContext):
    """Context for handling actions performed on startup and shutdown.

    It contains all the information required based on ASGI Lifespan Specification.

    Note:
        https://asgi.readthedocs.io/en/latest/specs/lifespan.html

    Attributes:
        type_ (str): type of context. Must be "lifespan".
        asgi_version (str): version of the ASGI spec.
        asgi_spec_version (str): The version of this spec being used. Optional; if
        missing defaults to "1.0".
        receive (Receive): ASGI receive function.
        send (Send): ASGI send function.
    """

    type_: str
    asgi_version: str
    asgi_spec_version: str
    receive: Receive
    send: Send

    @staticmethod
    def create(scope: Scope, receive: Receive, send: Send) -> LifespanContext:
        """Creates an instance of LifespanContext from ASGI args.

        Args:
            scope (Scope): ASGI scope.
            receive (Receive): ASGI receive function.
            send (Send): ASGI send function.

        Returns:
            LifespanContext: result.
        """
        return LifespanContext(
            type_=scope["type"],
            asgi_version=scope["asgi"]["version"],
            asgi_spec_version=scope["asgi"].get("spec_version", "1.0"),
            receive=receive,
            send=send,
        )


@dataclass
class HTTPContext(BaseContext):
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
    received_body: bool = False
    started: bool = False
    closed: bool = False

    @staticmethod
    def create(scope: Scope, receive: Receive, send: Send) -> "HTTPContext":
        """Create context from ASGI function args.

        Args:
            scope (Scope): ASGI scope.
            receive (Receive): ASGI receive.
            send (Send): ASGI send.

        Returns:
            HTTPContext: for storing info about request
        """
        return HTTPContext(
            request=HTTPRequest.create(scope),
            response=HTTPResponse.empty(),
            receive=receive,
            send=send,
        )

    def copy(self: "HTTPContext") -> "HTTPContext":
        """Create complete copy of HTTPContext.

        This function is needed to avoid side effects due to reference nature of Python
        when using `choose` combinator.

        Returns:
            HTTPContext: copy.
        """
        return HTTPContext(
            request=self.request.copy(),
            response=self.response.copy(),
            receive=self.receive,
            send=self.send,
            received_body=self.received_body,
            started=self.started,
            closed=self.closed,
        )


class ContextError(Exception, BaseContext):
    """Base class for `Exception`s that happen during handling `HTTPContext`.

    Attributes:
        ctx (HTTPContext): context that failed to be processed.
        message (str): message to respond.
        status (int): status code for response to send.

    Args:
        ctx (HTTPContext): context that failed to be processed.
        message (str): message to respond.
        status (int): status code for response to send.
    """

    def __init__(
        self,
        ctx: BaseContext,
        message: str = "Internal Server Error happened during handling request.",
        status=500,
    ) -> None:
        self.ctx = ctx
        self.message = message
        self.status = status
