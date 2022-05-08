from functools import wraps
from typing import Awaitable, Callable

from mona.core import BaseContext, ContextError, HTTPContext, LifespanContext
from mona.monads.future import Future

ContextResult = BaseContext | ContextError
Handler = Callable[[ContextResult], ContextResult | Awaitable[ContextResult]]


def error_handler(handler: Handler) -> Handler:
    """Decorator for `ContextError` handlers.

    This decorator will run handler only when `ContextError` is passed.
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

    This decorator will run this handler only when `HTTPContext` is passed.
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


def compose(*handlers: Handler) -> Handler:
    """Combinator for `Handler`s for sequential execution.

    Passed `Handler`s are executed one-by-one in passed oreder. Suitable for both sync
    and async handlers.

    Example::

        handler: Handler = compose(
            set_status(200_OK),
            set_header("Content-Type", "application/json"),
        )

        Future.create(Success(ctx)) >> handler

    Returns:
        HTTPHandler: resulting `HTTPHandler`.
    """
    return Future.compose(*handlers)


def choose(*handlers: Handler) -> Handler:
    """Combinator for choosing the first handler that returns `BaseContext`.

    Iterates through multiple passed `handlers` and returns first that returns
    `BaseContext`. If all handler return `ContextError` than returns initial
    `BaseContext`. If handlers are empty than return initial `BaseContext`.

    Example::

        handler = choose(
            # returns result if method is "GET" and path is "/user"
            get_dataclass('/user', User), # returns result if method is "GET" and path
            is "/users" get_dataclass('/users', Users),
        )

    Note:
        Handler `get_dataclass` from example are not real.

    Returns:
        Handler: resulting `Handler`.
    """
    # TODO replace with some more abstract @handler decorator
    @http_handler
    async def _choose(result: ContextResult) -> ContextResult:
        match handlers:
            case ():
                return result
            case some_handlers:
                for handler in some_handlers:
                    match await handler(result.copy()):
                        case ContextError():
                            continue
                        case ctx:
                            return ctx
                return result

    return _choose


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
