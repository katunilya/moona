from mona.core import ContextError, HTTPContext
from mona.handlers.body import send_body_text_async
from mona.handlers.core import error_handler
from mona.handlers.status import set_status
from mona.monads.future import Future


@error_handler
def send_error_async(err: ContextError) -> HTTPContext:
    """Default handler for all `HTTPContextErrors`.

    Sets response status to `err.status`, response body to `err.message`.

    Also sets headers:
    * Content-Length: XXX
    * Content-Type: text/plain
    """
    return (
        Future.create(err.ctx)
        >> set_status(err.status)
        >> send_body_text_async(err.message)
    )
