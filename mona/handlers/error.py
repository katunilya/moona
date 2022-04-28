from mona.core import HTTPContext


class HTTPContextError(Exception):
    """Base class for `Exception`s that happen during handling `HTTPContext`.

    Attributes:
        ctx (HTTPContext): context that failed to be processed.
        message (str): message to respond.
        status (int): status code for response to send.

    Args:
        ctx (HTTPContext): context that failed to be processed.
        message (str): message to respond.
        status (int): status code for response to send.
    """

    def __init__(
        self,
        ctx: HTTPContext,
        message: str = "Internal Server Error happened during handling request.",
        status=500,
    ) -> None:
        self.ctx = ctx
        self.message = message
        self.status = status
