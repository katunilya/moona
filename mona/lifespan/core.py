from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from mona.core import BaseContext, Message, Receive, Scope, Send
from mona.monads.pipe import Pipe


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

    @staticmethod
    def send(
        message: Message,
    ) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
        """`LifespanContext` sends passed message.

        Args:
            message (Message): to send.
        """

        async def _send(ctx: LifespanContext) -> LifespanContext:
            await ctx.__send(message)
            return ctx

        return _send

    def send_startup_complete_async(self) -> Awaitable[LifespanContext]:
        """Sends "lifespan.startup.complete" event.

        Note:
            [Docs](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#startup-complete-send-event)
        """
        return Pipe(self).then_future(
            LifespanContext.send({"type": "lifespan.startup.complete"})
        )

    def send_shutdown_complete_async(self) -> Awaitable[LifespanContext]:
        """Sends "lifespan.shutdown.complete" event.

        Note:
            [Docs](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#shutdown-complete-send-event)
        """
        return Pipe(self).then_future(
            LifespanContext.send({"type": "lifespan.shutdown.complete"})
        )

    @staticmethod
    def send_startup_failed_async(
        message: str = "",
    ) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
        """Send "lifespan.startup.failed" event.

        Args:
            message (str, optional): Info about reasons for failure. Defaults to "".
        """
        return LifespanContext.send(
            {"type": "lifespan.startup.failed", "message": message}
        )

    @staticmethod
    def send_shutdown_failed_async(
        message: str = "",
    ) -> Callable[[LifespanContext], Awaitable[LifespanContext]]:
        """Send "lifespan.shutdown.failed" event.

        Args:
            message (str, optional): Info about reasons for failure. Defaults to "".
        """
        return LifespanContext.send(
            {"type": "lifespan.shutdown.failed", "message": message}
        )

    def receive(self) -> Awaitable[Message]:
        """Receive some Message during handling "lifespan" scope.

        Returns:
            Awaitable[Message]: received message.
        """
        return self.__receive()
