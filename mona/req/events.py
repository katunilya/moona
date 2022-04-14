from mona import context, state


@state.accepts_right
async def receive_body(ctx: context.Context) -> context.Context:
    """Read entire request body and place it into context as ByteString."""
    body = b""
    more_body = True

    while more_body:
        message = await ctx.receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    ctx.request.body = body

    return context.right(ctx)
