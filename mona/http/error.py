from mona.core import ErrorContext
from mona.monads.future import Future
from mona.monads.pipe import Pipeline

from .body import set_response_body_text
from .core import HTTPContext, async_handler
from .events import send_response_body_async
from .status import set_status


@async_handler
def send_error_async(err: ErrorContext) -> Future[HTTPContext]:
    """Sends error when one happens in the system."""
    return (
        Pipeline(err.ctx)
        .then(set_status(err.status))
        .then(set_response_body_text(err.message))
        .then_future(send_response_body_async)
    )
