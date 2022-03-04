from mona import context, handler
from .body import parse_body_json


async def receive_body(ctx: context.Context) -> context.Context:
    """Read entire request body and place it into context as ByteString"""
    body = b""
    more_body = True

    while more_body:
        message = await ctx.receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    ctx.raw_request_body = body
    return ctx


# TODO make `receive_json` a function with docstring
receive_json = handler.compose(
    receive_body,
    parse_body_json,
)
