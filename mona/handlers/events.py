from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, http_handler


@http_handler
async def receive_body_async(ctx: HTTPContext) -> HTTPContextResult:
    """Handler "http.request" ASGI event, receive Request body.

    If body was already taken, than nothing would be done and `Success` `HTTPContext`
    would be returned. If at some point we receive "http.disconnect" event than
    `HTTPContext` is closed and `Success` `HTTPContext` returned.
    """
    match ctx.received_body:
        case True:
            return ctx
        case False:
            body = b""
            while True:
                match await ctx.receive():
                    case {"type": "http.request"} as message:
                        match message.get("more_body", False):
                            case True:
                                body += message.get("body", b"")
                            case False:
                                body += message.get("body", b"")
                                ctx.request.body = body
                                ctx.received_body = True
                                return ctx
                    case {"type": "http.disconnect"}:
                        ctx.closed = True
                        return ctx


@http_handler
async def send_response_start_async(ctx: HTTPContext) -> HTTPContextResult:
    """`HTTPContext` handler that sends "http.response.start" event to client."""
    match ctx.started:
        case True:
            return ctx
        case False:
            await ctx.send(
                {
                    "type": "http.response.start",
                    "status": ctx.response.status,
                    "headers": list(ctx.response.headers.items()),
                }
            )
            ctx.started = True
            return ctx


@http_handler
async def send_body_async(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sends "http.response.body" event to client.

    If "http.response.start" event was not send than it will be during execution of this
    handler.
    """
    ctx: HTTPContext = await (ctx >> send_response_start_async)
    await ctx.send({"type": "http.response.body", "body": ctx.response.body})
    ctx.closed = True
    return ctx
