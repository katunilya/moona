from mona.core import BaseContext, ContextError, HTTPContext, LifespanContext
from mona.handlers.core import (
    HTTPContextResult,
    LifespanContextResult,
    http_handler,
    lifespan_handler,
)


class WrongRequestType(ContextError):
    """`HTTPHandler` received `HTTPContext` of wrong type."""

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
            return WrongRequestType(ctx, "http")


@lifespan_handler
def lifespan(ctx: BaseContext) -> LifespanContextResult:
    """Handler that processes only `LifespanContext`."""
    match ctx:
        case LifespanContext():
            return ctx
        case _:
            return WrongRequestType(ctx, "lifespan")
