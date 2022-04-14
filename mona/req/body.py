from dataclasses import dataclass, is_dataclass
from typing import ByteString, Callable, Type

import orjson
from pydantic import BaseModel

from mona.context import Context
from mona.error import Error
from mona.state import RE, error, right


@dataclass
class RequestBodyIsNotReceivedError(Error):
    """Request body is None and cannot be taken."""

    message = "Request body is None and cannot be taken."
    code = 400

    def __init__(self):
        """Request body is None and cannot be taken."""


@dataclass
class TypeIsNotDataclassError(Error):
    """Passed type is not dataclass."""

    def __init__(self, t: Type):
        """Passed type is not dataclass.

        Args:
            t (Type): passed type
        """
        self.message = f"Type {t} is not dataclass."
        self.code = 500


@dataclass
class TypeIsNotPydanticBaseModel(Error):
    """Passed type is not `pydantic.BaseModel`."""

    def __init__(self, t: Type):
        """Passed type is not `pydantic.BaseModel`.

        Args:
            t (Type): passed type
        """
        self.message = f"Type {t} is not pydantic BaseModel."
        self.code = 500


def take_body(ctx: Context) -> RE[ByteString]:
    """Take request body as byte string."""
    if ctx.request.body is None:
        return error(RequestBodyIsNotReceivedError())

    return right(ctx.request.body)


def take_body_as_dict(ctx: Context) -> RE[dict]:
    """Take request body as dict."""
    if ctx.request.body is None:
        return error(RequestBodyIsNotReceivedError())

    return right(orjson.loads(ctx.request.body))


def take_body_as_dataclass(dataclass_type: Type) -> Callable[[Context], RE]:
    """Take request body as dataclass."""
    if not is_dataclass(dataclass_type):
        raise TypeIsNotDataclassError(dataclass_type)

    def _handler(ctx: Context) -> dataclass_type:
        if ctx.request.body is None:
            return error(RequestBodyIsNotReceivedError())

        return right(dataclass_type(**orjson.loads(ctx.request.body)))

    return _handler


def take_body_as_pydantic(
    model_type: Type[BaseModel],
) -> Callable[[Context], RE[BaseModel]]:
    """Take request body as pydantic BaseModel."""
    if not issubclass(model_type, BaseModel):
        raise TypeIsNotPydanticBaseModel(model_type)

    def _handler(ctx: Context) -> RE[model_type]:
        if ctx.request.body is None:
            return error(RequestBodyIsNotReceivedError())

        return right(model_type.parse_raw(ctx.request.body))

    return _handler


def take_body_as_str(ctx: Context) -> RE[str]:
    """Take request body as str."""
    if ctx.request.body is None:
        return error(RequestBodyIsNotReceivedError())

    return right(ctx.request.body.decode("UTF-8"))
