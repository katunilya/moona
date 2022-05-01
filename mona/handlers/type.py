from mona.core import HTTPContext, HTTPContextError
from mona.handlers.core import HTTPContextResult, http_handler


class WrongRequestType(HTTPContextError):
    """`HTTPHandler` received `HTTPContext` of wrong type."""

    def __init__(self, ctx: HTTPContext, type_: str) -> None:
        super().__init__(
            ctx,
            f"Wrong request type. Requires: {type_}. Received: {ctx.request.type_}.",
            500,
        )


@http_handler
def http(ctx: HTTPContext) -> HTTPContextResult:
    """`HTTPHandler` that processes only `HTTPContext` of "http" type."""
    match ctx.request.type_:
        case "http":
            return ctx
        case _:
            return WrongRequestType(ctx, "http")
