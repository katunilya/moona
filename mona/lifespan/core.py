from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Awaitable, Callable, TypeVar

from mona.core import BaseContext, ErrorContext, Message, Receive, Scope, Send
from mona.monads.future import Future
from mona.monads.pipe import Pipeline


@dataclass(slots=True)
class LifespanContext(BaseContext):
    """Context for handling actions performed on startup and shutdown.

    It contains all the information required based on ASGI Lifespan Specification.

    Note:
        https://asgi.readthedocs.io/en/latest/specs/lifespan.html

    Attributes:
        type_ (str): type of context. Must be "lifespan".
        asgi_version (str): version of the ASGI spec.
        asgi_spec_version (str): The version of this spec being used. Optional; if
        missing defaults to "1.0".
    """

    scope_type: str
    asgi_version: str
    asgi_spec_version: str
    __receive: Receive
    __send: Send

    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Creates an instance of `LifespanContext` from ASGI args.

        Args:
            scope (Scope): ASGI scope.
            receive (Receive): ASGI receive function.
            send (Send): ASGI send function.

        """
        self.scope_type = scope["type"]
        self.asgi_version = scope["asgi"]["version"]
        self.asgi_spec_version = scope["asgi"].get("spec_version", "1.0")
        self.__receive = receive
        self.__send = send


T = TypeVar("T")
V = TypeVar("V")


def handler(func: Callable[[T], V]) -> Callable[[LifespanContext], V | T]:
    """Decorator that protects sync function from non-`Lifespancontext` arg."""

    @wraps(func)
    def _wrapper(ctx: T) -> V | T:
        match ctx:
            case LifespanContext():
                return func(ctx)
            case other:
                return other

    return _wrapper


def async_handler(
    func: Callable[[T], Awaitable[V]]
) -> Callable[[LifespanContext], Awaitable[V | T]]:
    """Decorator that protects async function from non-`Lifespancontext` arg."""

    @wraps(func)
    async def _wrapper(ctx: T) -> V | T:
        match ctx:
            case LifespanContext():
                return await func(ctx)
            case other:
                return other

    return _wrapper


def send_async(
    message: Message,
) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
    """`LifespanContext` sends passed message.

    Args:
        message (Message): to send.
    """

    @async_handler
    async def _send(ctx: LifespanContext) -> LifespanContext:
        await ctx.__send(message)
        return ctx

    return _send


@async_handler
def send_startup_complete_async(ctx: LifespanContext) -> Awaitable[LifespanContext]:
    """Sends "lifespan.startup.complete" event.

    Note:
        [Docs](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#startup-complete-send-event)
    """
    return Pipeline(ctx).then_future(send_async({"type": "lifespan.startup.complete"}))


@async_handler
def send_shutdown_complete_async(ctx: LifespanContext) -> Awaitable[LifespanContext]:
    """Sends "lifespan.shutdown.complete" event.

    Note:
        [Docs](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#shutdown-complete-send-event)
    """
    return Pipeline(ctx).then_future(send_async({"type": "lifespan.shutdown.complete"}))


def send_startup_failed_async(
    message: str,
) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
    """Send "lifespan.startup.failed" event.

    Args:
        message (str, optional): Info about reasons for failure. Defaults to "".
    """
    return send_async({"type": "lifespan.startup.failed", "message": message})


def send_shutdown_failed_async(
    message: str,
) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
    """Send "lifespan.shutdown.failed" event.

    Args:
        message (str, optional): Info about reasons for failure. Defaults to "".
    """
    return send_async({"type": "lifespan.shutdown.failed", "message": message})


@async_handler
def receive_async(ctx: LifespanContext) -> Awaitable[Message]:
    """Receive some Message during handling "lifespan" scope.

    Returns:
        Awaitable[Message]: received message.
    """
    return ctx.__receive()


LifespanContextHandler = Callable[[LifespanContext], LifespanContext | ErrorContext]
AsyncLifespanContextHandler = Callable[
    [LifespanContext], Awaitable[LifespanContext | ErrorContext]
]


def lifespan_async(
    on_startup: AsyncLifespanContextHandler,
    on_shutdown: AsyncLifespanContextHandler,
) -> LifespanContextHandler:
    """Handler for "lifespan" scope type.

    `on_startup` is called on server startup receiving "lifespan.startup" event and
    `on_shutdown` is called on server shutdown receiving "lifespan.shutdown" event.

    Args:
        on_startup (LifespanHandler): to call on server startup.
        on_shutdown (LifespanHandler): to call on server shutdown.
    """

    @handler
    async def _lifespan_async(ctx: LifespanContext) -> LifespanContext:
        # This infinite loop ensures that lifespan scope persists over entire
        # application life cycle. Specific for "lifespan" scope.
        while True:
            match await ctx.__receive():
                case {"type": "lifespan.startup"}:
                    match await Future(on_startup(ctx)):
                        case LifespanContext():
                            await send_startup_complete_async(ctx)
                        case ErrorContext() as err:
                            await Pipeline(err.ctx).then_future(
                                send_startup_failed_async(err.message)
                            )
                case {"type": "lifespan.shutdown"}:
                    match await Future(on_shutdown(ctx)):
                        case LifespanContext():
                            await send_shutdown_complete_async(ctx)
                        case ErrorContext() as err:
                            await Pipeline(err.ctx).then_future(
                                send_shutdown_failed_async(err.message)
                            )
                    return ctx

    return _lifespan_async
