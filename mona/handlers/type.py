from mona.core import BaseContext, ErrorContext, HTTPContext
from mona.handlers.core import HTTPContextResult, http_handler


class WrongContextType(ErrorContext):
    """`Handler` received Context of wrong type."""

    def __init__(self, ctx: BaseContext, type_: str) -> None:
        super().__init__(
            ctx,
            f"Wrong request type. Requires: {type_}. Received: {str(ctx)}.",
            500,
        )


@http_handler
def http(ctx: BaseContext) -> HTTPContextResult:
    """Handler that processes only `HTTPContext`."""
    match ctx:
        case HTTPContext():
            return ctx
        case _:
            return WrongContextType(ctx, "http")
