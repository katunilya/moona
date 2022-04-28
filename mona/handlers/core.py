from typing import Awaitable, Callable

from mona.core import HTTPContext
from mona.handlers.error import HTTPContextError
from mona.monads.future import Future
from mona.monads.result import Failure, Result, Success

HTTPHandlerResult = Result[HTTPContext, HTTPContextError]
BaseHTTPHandler = Callable[
    [HTTPContext | HTTPContextError],
    Awaitable[HTTPContext | HTTPContextError] | HTTPContext | HTTPContextError,
]
HTTPHandler = Callable[
    [HTTPHandlerResult], Awaitable[HTTPHandlerResult] | HTTPHandlerResult
]


def http_handler(handler: BaseHTTPHandler) -> HTTPHandler:
    """Decorator for `HTTPContext` handlers.

    This decorator will run this handler only when `Success[HTTPContext]` is passed.
    Provides needed for switching from `Success` state to `Success` or `Failure`.
    """
    return Result.bound(handler)


def error_handler(handler: BaseHTTPHandler) -> HTTPHandler:
    """Decorator for `HTTPContextError` handlers.

    This decorator will run this handler only when `Failure[HTTPContextError]` is
    passed. Provides needed for switching from `Failure` state to `Success` or
    `Failure`.
    """
    return Result.altered(handler)


def compose(*handlers: HTTPHandler) -> HTTPHandler:
    """Combinator for `HTTPHandler`s for sequential execution.

    Passed `HTTPHandler`s are executed one-by-one in passed oreder.

    Example::

        handler: HTTPHandler = compose(
            set_status(200_OK),
            set_header("Content-Type", "application/json"),
        )

        Future.create(Success(ctx)) >> handler

    Returns:
        HTTPHandler: resulting `HTTPHandler`.
    """
    return Future.compose(*handlers)


def choose(*handlers: HTTPHandler) -> HTTPHandler:
    """Combinator for choosing the first handler that returns `Success`.

    Iterates through multiple passed `handlers` and returns first that returns
    `Success`. If no handler returns `Success` than returns initial `HTTPContext` as
    `Success`. If handlers are empty than return initial `HTTPContext` as `Success`
    result.

    Example::

        handler = choose(
            # returns result if method is "GET" and path is "/user"
            get_dataclass('/user', User),
            # returns result if method is "GET" and path is "/users"
            get_dataclass('/users', Users),
        )

    Returns:
        HTTPHandler: resulting `HTTPHandler`.
    """

    @http_handler
    async def _choose(ctx: HTTPContext) -> HTTPHandlerResult:
        match handlers:
            case ():
                return Success(ctx)
            case some_handlers:
                for handler in some_handlers:
                    match await (Future.create(ctx) >> HTTPContext.copy >> handler):
                        case Success() as success:
                            return success
                        case Failure():
                            continue
                return Success(ctx)

    return _choose
