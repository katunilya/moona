from functools import wraps
from typing import Awaitable, Callable

from mona.core import BaseContext, ContextError, HTTPContext, LifespanContext
from mona.monads.future import Future

ContextResult = BaseContext | ContextError
Handler = Callable[[ContextResult], ContextResult | Awaitable[ContextResult]]


def error_handler(handler: Handler) -> Handler:
    """Decorator for `ContextError` handlers.

    This decorator will run handler only when `ContextError` is
    passed.
    """

    @wraps(handler)
    def _error_handler(
        result: ContextResult,
    ) -> ContextResult | Awaitable[ContextResult]:
        match result:
            case ContextError() as err:
                return handler(err)
            case other:
                return other

    return _error_handler


HTTPContextResult = HTTPContext | ContextError
HTTPHandler = Callable[
    [HTTPContextResult], HTTPContextResult | Awaitable[HTTPContextResult]
]


def http_handler(handler: HTTPHandler) -> HTTPHandler:
    """Decorator for `HTTPContext` handlers.

    This decorator will run this handler only when `Success[HTTPContext]` is passed.
    Provides needed for switching from `Success` state to `Success` or `Failure`.
    """

    @wraps(handler)
    def _http_handler(
        result: HTTPContextResult,
    ) -> HTTPContextResult | Awaitable[HTTPContextResult]:
        match result:
            case HTTPContext() as ctx:
                match ctx.closed:
                    case True:
                        return ctx
                    case False:
                        return ctx >> handler
            case other:
                return other

    return _http_handler


def compose(*handlers: HTTPHandler) -> HTTPHandler:
    """Combinator for `HTTPHandler`s for sequential execution.

    Passed `HTTPHandler`s are executed one-by-one in passed oreder. Suitable for both
    sync and async handlers.

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
    async def _choose(result: HTTPContextResult) -> HTTPContextResult:
        match handlers:
            case ():
                return result
            case some_handlers:
                for handler in some_handlers:
                    match await (Future.create(result) >> HTTPContext.copy >> handler):
                        case HTTPContext() as ctx:
                            return ctx
                        case ContextError():
                            continue
                return result

    return _choose


def do(ctx: HTTPContextResult, *handlers: HTTPHandler) -> Future[HTTPContextResult]:
    """Execute multiple handlers on passed `HTTPContext` or `HTTPContextError`.

    If `HTTPContext` passed than it is automatically wrapped into `Success`. If
    `HTTPContextError` than it is wrapped into `Failure`.

    Note:
        This is possible syntax for executing multiple functions, but `>>` is more
        supported.

    Args:
        ctx (HTTPContext | HTTPContextError | HTTPContextResult): to use as argument.

    Returns:
        Future[HTTPContextResult]: result.
    """
    return Future.do(ctx, *handlers)


LifespanContextResult = LifespanContext | ContextError
LifespanHandler = Callable[
    [LifespanContextResult], LifespanContextResult | Awaitable[LifespanContextResult]
]


def lifespan_handler(handler: LifespanHandler) -> LifespanHandler:
    """Decorator for `LifespanContext` handlers on startup and shutdown.

    This decorator will proceed only unfinished `LifespanContext`.
    """

    @wraps(handler)
    def _lifespan_handler(result: LifespanContextResult) -> LifespanContextResult:
        match result:
            case LifespanContext() as ctx:
                return ctx >> handler
            case other:
                return other

    return _lifespan_handler
