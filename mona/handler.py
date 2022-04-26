import functools
import typing

from mona import types
from mona.monads import future, state

SyncHandler = typing.Callable[[types.StateContext], types.StateContext]
AsyncHandler = typing.Callable[
    [types.StateContext], typing.Awaitable[types.StateContext]
]
Handler = SyncHandler | AsyncHandler


def __continue_on_not_right(current_handler: Handler, next_handler: Handler) -> Handler:
    @state.accepts_right
    async def __continuation(ctx: types.Context) -> types.StateContext:
        match await (
            future.from_value(ctx) >> types.copy >> state.Right >> current_handler
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
    match handlers:
        case ():
            return future.identity
        case _:
            return functools.reduce(__continue_on_not_right, handlers)
