import typing

import orjson
import pydantic
import toolz

from mona import context, error, future, handler, state

from . import header, status


def set_body_bytes(body: typing.ByteString) -> handler.Handler:
    """Set response body from byte string."""

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.body = body
        return state.right(ctx)

    return _handler


def set_body_text(body: str) -> handler.Handler:
    """Set response body from string."""
    body = body.encode("UTF-8")

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.body = body
        return state.right(ctx)

    return _handler


def set_body_from_bytes(
    function: typing.Callable[
        [context.Context], future.Future[state.RE[typing.ByteString]]
    ]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        body: state.RE[dict] = await (future.from_value(ctx) >> function)

        if body.state != state.RIGHT:
            err: error.Error = body.value

            return toolz.pipe(
                ctx,
                state.right,
                set_body_text(err.message),
                status.set_status_bad_request,
                state.switch_error,
            )

        return toolz.pipe(
            ctx,
            state.right,
            set_body_bytes(body.value),
        )

    return _handler


def set_body_from_text(
    function: typing.Callable[[context.Context], future.Future[state.RE[str]]]
) -> handler.Handler:
    """Set body from function calculation result (str)."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        body: state.RE[str] = await (future.from_value(ctx) >> function)

        if body.state == state.ERROR:
            err: error.Error = body.value

            return toolz.pipe(
                ctx,
                state.right,
                set_body_text(err.message),
                status.set_status_bad_request,
                state.switch_error,
            )

        return toolz.pipe(
            ctx,
            state.right,
            set_body_bytes(body.value.encode("UTF-8")),
        )

    return _handler


def set_body_from_dict(
    function: typing.Callable[[context.Context], future.Future[state.RE[dict]]]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        body: state.RE[dict] = await (future.from_value(ctx) >> function)

        if body.state != state.RIGHT:
            err: error.Error = body.value

            return toolz.pipe(
                ctx,
                state.right,
                set_body_text(err.message),
                status.set_status_bad_request,
                state.switch_error,
            )

        return toolz.pipe(
            ctx,
            state.right,
            set_body_bytes(orjson.dumps(body.value)),
            header.set_header("Content-Type", "application/json"),
            status.set_status_ok,
        )

    return _handler


def set_body_from_pydantic(
    function: typing.Callable[
        [context.Context], future.Future[state.RE[pydantic.BaseModel]]
    ]
) -> handler.Handler:
    """Set body from function calculation result."""

    @state.accepts_right
    async def _handler(ctx: context.Context) -> context.StateContext:
        body: state.RE[pydantic.BaseModel] = await (future.from_value(ctx) >> function)

        if body.state != state.RIGHT:
            err: error.Error = body.value

            return toolz.pipe(
                ctx,
                state.right,
                set_body_text(err.message),
                status.set_status_bad_request,
                state.switch_error,
            )

        return toolz.pipe(
            ctx,
            state.right,
            set_body_bytes(orjson.dumps(body.value.dict())),
            header.set_header("Content-Type", "application/json"),
            status.set_status_ok,
        )

    return _handler
