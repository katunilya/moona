from mona import types
from mona.monads import state


@state.accepts_right
async def send_start(ctx: types.Context) -> types.StateContext:
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
async def send_body(ctx: types.Context) -> types.StateContext:
    """Send response body event, which closes connection between server and client."""
    await ctx.send(
        {
            "type": "http.response.body",
            "body": ctx.response.body,
        }
    )
    return state.Final(ctx)
