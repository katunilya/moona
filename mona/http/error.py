from mona.core import ErrorContext
from mona.handlers.status import set_status
from mona.http.core import HTTPContext
from mona.monads.future import Future
from mona.monads.pipe import Pipeline


def send_error_async(err: ErrorContext) -> Future[HTTPContext]:
    return Pipeline(err.ctx).then(set_status(err.status))
