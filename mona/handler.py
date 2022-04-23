import functools
import typing

from mona import context
from mona.monads import future, state

SyncHandler = typing.Callable[[context.StateContext], context.StateContext]
AsyncHandler = typing.Callable[
    [context.StateContext], typing.Awaitable[context.StateContext]
]
Handler = SyncHandler | AsyncHandler


def __continue_on_not_right(current_handler: Handler, next_handler: Handler) -> Handler:
    @state.accepts_right
    async def __continuation(ctx: context.Context) -> context.StateContext:
        match await (
            future.from_value(ctx) >> context.copy >> state.Right >> current_handler
        ):
            case state.Right(value):
                return value
            case _:
                return await (future.from_value(ctx) >> state.Right >> next_handler)

    return __continuation


def choose(*handlers: Handler) -> Handler:
    """Chooses the first handler to return ctx in right state.

    Returns:
        Handler: choose composition handler
    """
    if len(handlers) > 0:
        return functools.reduce(__continue_on_not_right, handlers)
    else:
        return future.identity
