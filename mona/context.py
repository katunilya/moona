from typing import Any, Awaitable, ByteString, Dict, Iterable, Optional

from mona import future, state, types


class Context:
    """Request handling context that stores all the required for computation info.

    Instance of `Context` is constructed every time request is received by ASGI.
    Initially it takes and parses `scope` information, `receive` and `send` functions.
    It is suitable for both HTTP and WebSocket connections. To be minimal in terms of
    weight and efficiency it has a strict set of predefined `__slots__`.
    """

    __slots__ = (
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
        "receive",
        "send",
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
        scope: types.Scope,
        receive: types.Receive,
        send: types.Send,
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
        self.receive: types.Receive = receive
        self.send: types.Send = send
        # custom
        self.subprotocols: Iterable[str] = []
        self.raw_request_body: ByteString = None
        self.request_body: Any = None
        self.request_headers: Dict[str, str] = None
        self.query: Dict[str, str] = None
        self.params: Dict[str, str] = None
        # response
        self.response_status: int = 200
        self.response_body: ByteString = b""
        self.response_headers: Dict[str, str] = {}


StateContext = state.State[Context]
FutureStateContext = Awaitable[StateContext]
Handler = types.Transform[StateContext, FutureStateContext]


async def pack(ctx: Context) -> StateContext:
    """Wraps `context.Context` into `State` and `Future` monad."""
    return state.pack(await future.pack(ctx))


async def bind(handler: Handler, ctx: FutureStateContext) -> StateContext:
    """Executes `context.Handler` considering `State` and `Future`."""
    ctx: StateContext = await pack(ctx)

    if ctx.valid:
        ctx = handler(ctx.value)

    return state.pack(await future.pack(ctx))
