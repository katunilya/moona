from typing import Type

from pydantic import BaseModel

from mona import context, handler

from .body import (
    parse_json_to_dataclass,
    parse_json_to_dict,
    parse_json_to_pydantic,
    parse_to_string,
)


async def receive_body(ctx: context.Context) -> context.Context:
    """Read entire request body and place it into context as ByteString"""
    body = b""
    more_body = True

    while more_body:
        message = await ctx.receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    ctx.raw_request_body = body
    return ctx


async def receive_json_dict(ctx: context.Context) -> context.Context:
    """Read entire request body and parse it directly to dict from json string."""
    # TODO [OPTIONAL] for optimization purpose this might be done directly, but it will
    #                 be harder to support this code in future
    _handler = handler.compose(
        receive_body,
        parse_json_to_dict,
    )

    return await _handler(ctx)


def receive_json_dataclass(dataclass_: Type) -> context.Handler:
    """Read entire request body and parse it directly to dataclass from json string."""

    return handler.compose(
        receive_body,
        parse_json_to_dataclass(dataclass_),
    )


def receive_json_pydantic(pydantic_model: Type[BaseModel]) -> context.Handler:
    """Read entire request body and parse it directly to `BaseModel` from json."""

    return handler.compose(
        receive_body,
        parse_json_to_pydantic(pydantic_model),
    )


async def receive_string(ctx: context.Context) -> context.Context:
    """Read entire request body and decode it to string with UTF-8."""
    # TODO [OPTIONAL] for optimization purpose this might be done directly, but it will
    #                 be harder to support this code in future
    _handler = handler.compose(
        receive_body,
        parse_to_string,
    )

    return await _handler(ctx)
