from mona import context


async def send_start(ctx: context.Context) -> context.Context:
    """Send response start event according to ASGI specification."""
    await ctx.send(
        {
            "type": "http.response.start",
            "status": ctx.response_status,
            "headers": [
                (key.encode("utf-8"), value.encode("utf-8"))
                for key, value in ctx.response_headers.items()
            ],
        }
    )
    return ctx


async def send_body(ctx: context.Context) -> context.Context:
    """Send response body event, which closes connection between server and client."""
    await ctx.send(
        {
            "type": "http.response.body",
            "body": ctx.response_body,
        }
    )
    return ctx
