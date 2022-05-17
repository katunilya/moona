from pymon.core import Future, Pipe

from moona.http.context import (
    HTTPContext,
    send_message,
    set_closed,
    set_received,
    set_started,
)
from moona.http.handlers import HTTPFunc, handle_func, handler, skip

# handlers


@handler
def start(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Send message to client and return `HTTPContext` that sent that.

    Args:
        nxt (HTTPHandler): next handler.
        ctx (HTTPContext): actor.
    """
    match ctx.started:
        case True:
            return nxt(ctx)
        case False:
            message = {
                "type": "http.response.start",
                "headers": list(ctx.response_headers.items()),
                "status": ctx.response_status,
            }
            return Pipe(ctx) << set_started(True) >> send_message(message) >> nxt


@handle_func
def respond(ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Send response body to the client and close the context.

    Args:
        nxt (HTTPFunc): to execute next.
        ctx (HTTPContext): context to send body from.
    """
    return (
        Pipe(ctx)
        << set_closed(True)
        >> send_message({"type": "http.response.body", "body": ctx.response_body})
    )


@handler
async def receive(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
    """Receive request body from client.

    Args:
        nxt (HTTPFunc): to execute next if body had been successfully received..
        ctx (HTTPContext): to write body to.
    """
    match ctx.received:
        case False:
            msg = await ctx.receive()
            match msg:
                case {"type": "http.request"}:
                    ctx.request_body += msg["body"]
                    match msg.get("more_body", False):
                        case True:
                            return await receive(nxt, ctx)
                        case False:
                            return await (Pipe(ctx) << set_received(True) >> nxt)
                case {"type": "http.disconnect"}:
                    return await (Pipe(ctx) << set_closed(True) >> skip)
        case True:
            return await nxt(ctx)
