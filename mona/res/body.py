import typing

import orjson
import pydantic

from mona import context, future, handler, state

from . import header, status


def set_body_bytes(body: bytes) -> handler.Handler:
    """Set response body from byte string."""

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.body = body
        return state.Right(ctx)

    return _handler


def set_body_text(body: str) -> handler.Handler:
    """Set response body from string."""
    body = body.encode("UTF-8")

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.body = body
        return state.Right(ctx)

    return _handler


def set_body_from_bytes(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[bytes]]]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        match await (future.from_value(ctx) >> function):
            case state.Error(err):
                return (
                    state.Right(ctx)
                    >> set_body_text(str(err))
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )
            case state.Right(bytes() as body):
                return state.Right(ctx) >> set_body_bytes(body)
            case other:
                return (
                    state.Right(ctx)
                    >> set_body_text(f"Cannot set body from: {other}")
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error,
                )

    return _handler


def set_body_from_text(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[str]]]
) -> handler.Handler:
    """Set body from function calculation result (str)."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        match await (future.from_value(ctx) >> function):
            case state.Error(err):
                return (
                    state.Right(ctx)
                    >> set_body_text(str(err))
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )
            case state.Right(str() as body):
                return (
                    state.Right(ctx)
                    >> set_body_bytes(body.encode("UTF-8"))
                    >> header.set_header_content_type_text_plain
                )
            case other:
                return (
                    state.Right(ctx)
                    >> set_body_text(f"Cannot set body from: {other}")
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )

    return _handler


def set_body_from_dict(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[dict]]]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        match await (future.from_value(ctx) >> function):
            case state.Error(err):
                return (
                    state.Right(ctx)
                    >> set_body_text(str(err))
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )
            case state.Right(value=dict(body)):
                return (
                    state.Right(ctx)
                    >> set_body_bytes(orjson.dumps(body))
                    >> header.set_header_content_type_application_json
                )
            case other:
                return (
                    state.Right(ctx)
                    >> set_body_text(f"Cannot set body from {other}")
                    >> state.switch_to_error
                )

    return _handler


def set_body_from_pydantic(
    function: typing.Callable[
        [context.Context], future.Future[state.ESafe[pydantic.BaseModel]]
    ]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        match await (future.from_value(ctx) >> function):
            case state.Error(err):
                return (
                    state.Right(ctx)
                    >> set_body_text(str(err))
                    >> header.set_header_content_type_text_plain
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )
            case state.Right(pydantic.BaseModel() as body):
                return (
                    state.Right(ctx)
                    >> set_body_bytes(orjson.dumps(body.dict()))
                    >> header.set_header_content_type_application_json
                )
            case other:
                return (
                    state.Right(ctx)
                    >> set_body_from_text(f"Cannot set body from {other}")
                    >> status.set_status_internal_server_error
                    >> state.switch_to_error
                )

    return _handler
