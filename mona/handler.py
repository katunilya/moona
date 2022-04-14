import functools
import typing

from mona import context, future, state

SyncHandler = typing.Callable[[context.StateContext], context.StateContext]
AsyncHandler = typing.Callable[
    [context.StateContext], typing.Awaitable[context.StateContext]
]
Handler = typing.Union[SyncHandler, AsyncHandler]


def __continue_on_fail(current_handler: Handler, next_handler: Handler) -> Handler:
    @state.accepts_right
    async def __continuation(ctx: context.Context) -> context.StateContext:
        ctx_copy = state.right(context.copy(ctx))

        ctx_copy: context.StateContext = await (
            future.from_value(ctx_copy) >> current_handler
        )

        if ctx_copy.state != state.RIGHT:
            return await (future.from_value(state.right(ctx)) >> next_handler)

        return ctx_copy

    return __continuation


def choose(*handlers: Handler) -> Handler:
    """Chooses the first handler to return ctx in right state.

    Returns:
        Handler: choose composition handler
    """
    return (
        functools.reduce(__continue_on_fail, handlers)
        if len(handlers) > 0
        else future.identity
    )
