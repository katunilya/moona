from .types import ASGIContext, ASGIHandler


def set(key: str, value: str) -> ASGIHandler:
    """Generates handler that sets passed key value pair into response headers."""

    def _handler(context: ASGIContext) -> ASGIContext:
        context.response_headers[key] = value
        return context

    return _handler
