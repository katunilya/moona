from mona.core import ContextError, LifespanContext
from mona.handlers.core import LifespanHandler, lifespan_handler
from mona.monads.future import Future


def lifespan_async(
    on_startup: LifespanHandler, on_shutdown: LifespanHandler
) -> LifespanHandler:
    """Handler for "lifespan" scope type.

    `on_startup` is called on server startup receiving "lifespan.startup" event and
    `on_shutdown` is called on server shutdown receiving "lifespan.shutdown" event.

    Args:
        on_startup (LifespanHandler): to call on server startup.
        on_shutdown (LifespanHandler): to call on server shutdown.
    """

    @lifespan_handler
    async def _lifespan_async(ctx: LifespanContext) -> LifespanContext:
        # This infinite loop ensures that lifespan scope persists over entire
        # application life cycle. Specific for "lifespan" scope.
        while True:
            match await ctx.receive():
                case {"type": "lifespan.startup"}:
                    result = await (Future.create(ctx) >> on_startup)
                    match result:
                        case LifespanContext():
                            await ctx.send({"type": "lifespan.startup.complete"})
                        case ContextError() as err:
                            await ctx.send(
                                {
                                    "type": "lifespan.startup.failed",
                                    "message": err.message,
                                }
                            )
                case {"type": "lifespan.shutdown"}:
                    result = await (Future.create(ctx) >> on_shutdown)
                    match result:
                        case LifespanContext():
                            await ctx.send({"type": "lifespan.shutdown.complete"})
                        case ContextError() as err:
                            await ctx.send(
                                {
                                    "type": "lifespan.shutdown.failed",
                                    "message": err.message,
                                }
                            )
                    return result

    return _lifespan_async
