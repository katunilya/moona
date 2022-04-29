from mona.core import HTTPContext
from mona.handlers.core import HTTPHandlerResult, http_handler
from mona.monads.result import Success


@http_handler
async def receive_body(ctx: HTTPContext) -> HTTPHandlerResult:
    """Handler "http.request" ASGI event, receive Request body.

    If body was already taken, than nothing would be done and `Success` `HTTPContext`
    would be returned. If at some point we receive "http.disconnect" event than
    `HTTPContext` is closed and `Success` `HTTPContext` returned.
    """
    match ctx.closed, ctx.received_body:
        case True, _:
            return Success(ctx)
        case False, True:
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
                                return Success(ctx)
                    case {"type": "http.disconnect"}:
                        ctx.closed = True
                        return Success(ctx)
        case False, False:
            return Success(ctx)


@http_handler
async def send_body(ctx: HTTPContext) -> HTTPHandlerResult:
    """Handler that sends "http.response.body" event to client."""
    match ctx.closed:
        case True:
            return Success(ctx)
        case False:
            await ctx.send({"type": "http.response.body", "body": ctx.response.body})
            ctx.closed = True
            return Success(ctx)


@http_handler
async def send_response_start(ctx: HTTPContext) -> HTTPHandlerResult:
    """`HTTPContext` handler that sends "http.response.start" event to client."""
    match ctx.closed, ctx.started:
        case True, _:
            return Success(ctx)
        case False, True:
            return Success(ctx)
        case False, False:
            await ctx.send(
                {
                    "type": "http.response.start",
                    "status": ctx.response.status,
                    "headers": ctx.response.headers,
                }
            )
            ctx.started = True
            return ctx
