from mona import context, handler
from mona.monads import state


def set_header(key: str, value: str) -> handler.Handler:
    """Generates handler that sets passed key value pair into response headers."""
    key = key.encode("UTF-8")
    value = value.encode("UTF-8")

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.headers[key] = value
        return state.Right(ctx)

    return _handler


def set_header_content_type(value: str) -> handler.Handler:
    """Sets value for `Content-Type` header of response."""
    return set_header("Content-Type", value)


set_header_content_type_application_json = set_header_content_type("application/json")
set_header_content_type_text_plain = set_header_content_type("text/plain")
