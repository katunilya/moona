from mona import context
from mona.monads import state


@state.accepts_right
async def send_start(ctx: context.Context) -> context.StateContext:
    """Send response start event accroding to ASGI specs."""
    headers = list(ctx.response.headers.items())

    await ctx.send(
        {
            "type": "http.response.start",
            "status": ctx.response.status,
            "headers": headers,
        }
    )

    return state.Right(ctx)


@state.accepts_right
async def send_body(ctx: context.Context) -> context.StateContext:
    """Send response body event, which closes connection between server and client."""
    await ctx.send(
        {
            "type": "http.response.body",
            "body": ctx.response.body,
        }
    )
    return state.Final(ctx)
