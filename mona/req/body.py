import dataclasses
from typing import Type

import orjson
from pydantic import BaseModel

from mona import context


def parse_json_to_dict(ctx: context.Context) -> context.Context:
    """When raw request body is not `None` try parse it to `Dict`."""
    if ctx.raw_request_body is not None:
        ctx.request_body = orjson.loads(ctx.raw_request_body)

    return ctx


def parse_json_to_dataclass(dataclass_: Type) -> context.Handler:
    """When raw request body is not `None` parse it to passed dataclass."""

    # TODO get rid of assert as it is unsafe
    assert dataclasses.is_dataclass(dataclass_)

    def _handler(ctx: context.Context) -> context.Context:
        if ctx.raw_request_body is not None:
            ctx.request_body = dataclass_(**orjson.loads(ctx.raw_request_body))
        return ctx

    return _handler


def parse_json_to_pydantic(pydantic_model: Type[BaseModel]) -> context.Context:
    """When raw request body is not `None` parse it to passed `pydantic.BaseModel`."""

    # TODO get rid of assert as it is unsafe
    assert issubclass(pydantic_model, BaseModel)

    def _handler(ctx: context.Context) -> context.Context:
        if ctx.raw_request_body is not None:
            ctx.request_body = pydantic_model.parse_raw(ctx.raw_request_body)
        return ctx

    return _handler


def parse_to_string(ctx: context.Context) -> context.Context:
    """When raw request body is not `None` decode it to string with UTF-8."""
    if ctx.raw_request_body is not None:
        ctx.request_body = ctx.raw_request_body.decode("utf-8")

    return ctx
