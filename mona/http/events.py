from email import message

from mona.http.core import (
    HTTPContext,
    async_handler,
    get_response_body,
    receive_async,
    send_async,
    set_closed_true,
    set_received_true,
    set_started_true,
)
from mona.monads.future import Future
from mona.monads.maybe import Maybe
from mona.monads.pipe import Pipeline


@async_handler
def send_response_start_async(ctx: HTTPContext) -> Future[HTTPContext]:
    """Send "http.response.start" event based on `HTTPContext` values.

    Sends headers and status code. Should be sent before response body.
    """
    match ctx.started:
        case False:
            return (
                Pipeline(ctx)
                .then_future(
                    send_async(
                        {
                            "type": "http.respose.start",
                            "status": ctx.response_status,
                            "headers": ctx.response_headers,
                        }
                    )
                )
                .then(set_started_true)
            )
        case True:
            return Future.this(ctx)


@async_handler
def send_response_body_async(ctx: HTTPContext) -> Future[HTTPContext]:
    """Send "http.respose.body" event based on `HTTPContext` values.

    Also attempts to send "http.respose.start" in case it was not sent.
    """
    match ctx.closed:
        case False:
            return (
                Pipeline(ctx)
                .then_future(send_response_start_async)
                .then_future(
                    send_async(
                        {
                            "type": "http.respose.body",
                            "body": Pipeline(ctx)
                            .then(get_response_body)
                            .then_maybe(Maybe.this)
                            .return_some_or(b""),
                        }
                    )
                )
                .then(set_closed_true)
            )
        case True:
            return Future.this(ctx)


@async_handler
async def receive_body_async(ctx: HTTPContext) -> HTTPContext:
    """Receive "http.request" event from client and write body to `HTTPContext`.

    If body had been already taken then nothing would be done and `HTTPContext` would be
    just returned. If we receive "http.disconnect" than `HTTPContext` is closed and
    won't be processed next.
    """
    match ctx.received:
        case True:
            return ctx
        case False:
            body = b""
            while True:
                match await receive_async(ctx):
                    case {"type": "http.request"} as msg:
                        match msg.get("more_body", False):
                            case True:
                                body += msg.get("body", b"")
                            case False:
                                body += message.get("body", b"")
                                ctx.request_body = body
                                return set_received_true(ctx)
                    case {"type": "http.disconnect"}:
                        return set_closed_true(ctx)
