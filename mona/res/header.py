from mona import context


def set_header(key: str, value: str) -> context.Handler:
    """Generates handler that sets passed key value pair into response headers."""

    def _handler(ctx: context.Context) -> context.Context:
        ctx.response_headers[key] = value
        return ctx

    return _handler


def set_header_content_type(value: str) -> context.Handler:
    """Sets value for `Content-Type` header of response."""
    return set_header("Content-Type", value)
