from typing import Awaitable, ByteString, Callable, Dict, Optional

from black import Any
from typeguard import Iterable
from typing_extensions import TypeAlias

from mona import state, types

Message: TypeAlias = Dict[str, Any]
Scope: TypeAlias = Message
Receive: TypeAlias = types.Construct[Awaitable[Message]]
Send: TypeAlias = types.Transform[Message, Awaitable[None]]
ASGIServer: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]


class ASGIContext:
    """Request handling context that stores all the required for computation info.

    Instance of `Context` is constructed every time request is received by ASGI.
    Initially it takes and parses `scope` information, `receive` and `send` functions.
    It is suitable for both HTTP and WebSocket connections. To be minimal in terms of
    weight and efficiency it has a strict set of predefined `__slots__`.
    """

    __slots__ = (
        # default scope information
        "type",
        "asgi_version",
        "asgi_spec_version",
        "http_version",
        "method",
        "scheme",
        "path",
        "raw_path",
        "query_string",
        "root_path",
        "raw_headers",
        "client_host",
        "client_port",
        "server_host",
        "server_port",
        "raw_subprotocols",
        # functions
        "receive",
        "send",
        # custom
        "subprotocols",
        "raw_request_body",
        "request_body",
        "request_headers",
        "query",
        "params",
        "response_status",
        "response_body",
        "response_headers",
    )

    def __init__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        self.type: str = scope["type"]
        self.asgi_version: str = scope["asgi"]["version"]
        self.asgi_spec_version: str = scope["asgi"]["spec_version"]
        self.http_version: str = scope["http_version"]
        self.method: Optional[str] = scope.get("method", None)
        self.scheme: str = scope["scheme"]
        self.path: str = scope["path"]
        self.raw_path: ByteString = scope["raw_path"]
        self.query_string: ByteString = scope["query_string"]
        self.root_path: str = scope["root_path"]
        self.raw_headers: Iterable[ByteString, ByteString] = scope["headers"]
        self.client_host: str = scope["client"][0]
        self.client_port: int = scope["client"][1]
        self.server_host: str = scope["server"][0]
        self.server_port: Optional[int] = scope["server"][1]
        self.raw_subprotocols: Optional[Iterable[str]] = scope.get("subprotocols", None)
        # functions
        self.receive: Receive = receive
        self.send: Send = send
        # custom
        self.subprotocols: Iterable[str] = []
        self.raw_request_body: ByteString = None
        self.request_body: Any = None
        self.request_headers: Dict[str, str] = None
        self.query: Dict[str, str] = None
        self.params: Dict[str, str] = None
        # response
        self.response_status: int = 200
        self.response_body: Any = None
        self.response_headers: Dict[str, str] = {}


ASGIHandler = types.Transform[ASGIContext, Awaitable[state.State[ASGIContext]]]
