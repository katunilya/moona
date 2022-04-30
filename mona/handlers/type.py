from mona.core import HTTPContext
from mona.handlers.core import HTTPHandlerResult, http_handler
from mona.handlers.error import HTTPContextError
from mona.monads.result import Failure, Success


class WrongRequestType(HTTPContextError):
    """`HTTPHandler` received `HTTPContext` of wrong type."""

    def __init__(self, ctx: HTTPContext, type_: str) -> None:
        super().__init__(
            ctx,
            f"Wrong request type. Requires: {type_}. Received: {ctx.request.type_}.",
            500,
        )


@http_handler
def on_http(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPHandler` that processes only `HTTPContext` of "http" type."""
    match ctx.request.type_:
        case "http":
            return Success(ctx)
        case _:
            return Failure
