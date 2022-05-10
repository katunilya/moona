from mona.core import ErrorContext, HTTPContext
from mona.handlers.body import send_body_text_async
from mona.handlers.core import error_handler
from mona.handlers.status import set_status
from mona.monads.future import Future


@error_handler
def send_error_async(err: ErrorContext) -> Future[HTTPContext]:
    """Default handler for all `HTTPContextErrors`.

    Sets response status to `err.status`, response body to `err.message`.

    Also sets headers:
    * Content-Length: XXX
    * Content-Type: text/plain
    """
    return (
        Future.from_value(err.ctx)
        .then(set_status(err.status))
        .then_future(send_body_text_async(err.message))
    )
