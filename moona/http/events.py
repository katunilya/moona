from pymon.core import Future, Pipe, returns_future

from moona.context import Message
from moona.http.context import HTTPContext, set_closed, set_started
from moona.http.handlers import HTTPFunc, handler, skip


# funcs
def send_message_async(message: Message) -> HTTPFunc:
    """`HTTPFunc` that sends passed message to client.

    Args:
        message (Message): to send to the client.
    """

    @returns_future
    async def func(ctx: HTTPContext) -> HTTPContext:
        await ctx.send(message)
        return ctx

    return func


# handlers


@handler
def start_response(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Send message to client and return `HTTPContext` that sent that.

    Args:
        nxt (HTTPHandler): next handler.
        ctx (HTTPContext): actor.
    """
    match ctx.started:
        case True:
            return nxt(ctx)
        case False:
            return (
                Pipe(ctx)
                >> send_message_async(
                    {
                        "type": "http.response.start",
                        "headers": ctx.response_headers,
                        "status": ctx.response_status,
                    }
                )
                << set_started(True)
                >> nxt
            )


def send_body(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Send response body to the client and close the context.

    Args:
        nxt (HTTPFunc): to execute next.
        ctx (HTTPContext): context to send body from.
    """

    def _handler(_nxt: HTTPFunc, _ctx: HTTPContext) -> Future[HTTPContext | None]:
        match _ctx.closed:
            case True:
                return _nxt(ctx)
            case False:
                return (
                    Pipe(ctx)
                    << set_closed(True)
                    >> send_message_async(
                        {"type": "http.response.body", "body": ctx.response_body}
                    )
                    >> _nxt
                )

    return (start_response >> _handler)(nxt, ctx)


@handler
async def receive_body(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
    """Receive request body from client.

    Args:
        nxt (HTTPFunc): to execute next if body had been successfully received..
        ctx (HTTPContext): to write body to.
    """
    msg = await ctx.receive()
    match msg:
        case {"type": "http.request"}:
            ctx.request_body += msg["body"]
            match msg.get("more_body", False):
                case True:
                    return receive_body(nxt, ctx)
                case False:
                    return nxt(ctx)
        case {"type": "http.disconnect"}:
            return Pipe(ctx) << set_closed(True) >> skip
