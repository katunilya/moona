from __future__ import annotations

from dataclasses import dataclass

from moona.context import BaseContext, Receive, Scope, Send


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
        self.receive = receive
        self.send = send
