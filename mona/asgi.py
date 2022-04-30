from mona.core import ASGIApp, HTTPContext, Receive, Scope, Send
from mona.handlers.body import set_body_text
from mona.handlers.core import HTTPContextResult, HTTPHandler
from mona.handlers.error import HTTPContextError
from mona.handlers.events import send_body, send_response_start
from mona.handlers.status import set_status
from mona.monads.future import Future
from mona.monads.result import Failure, Success


def create(handler: HTTPHandler) -> ASGIApp:
    """Constructs ASGI Server function from sequence of handlers.

    Notes:
        * https://asgi.readthedocs.io/en/latest/specs/main.html#applications

    Returns:
        ASGIApp: ASGI function based on ASGI Specification.
    """

    async def _asgi(scope: Scope, receive: Receive, send: Send) -> None:
        result: HTTPContextResult = await (
            Future.create(HTTPContext.create(scope, receive, send))
            >> Success
            >> handler
        )
        match result:
            case Success(value=HTTPContext() as ctx):
                match ctx.started, ctx.closed:
                    case True, True:
                        # started and closed
                        return
                    case True, False:
                        # started, but not closed (response not send)
                        await (Future.create(ctx) >> Success >> send_body)
                    case False, _:
                        await (
                            Future.create(ctx)
                            >> Success
                            >> send_response_start
                            >> send_body
                        )
            case Failure(value=HTTPContextError() as err):
                match err.ctx.started, err.ctx.closed:
                    case True, True:
                        return
                    case True, False:
                        await (
                            Future.create()
                            >> Success
                            >> set_body_text(err.message)
                            >> send_body
                        )
                    case False, _:
                        await (
                            Future.create(err.ctx)
                            >> Success
                            >> set_status(err.status)
                            >> set_body_text(err.message)
                            >> send_response_start
                            >> send_body
                        )

    return _asgi
