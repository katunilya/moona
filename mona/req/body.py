import dataclasses
import typing

import orjson
import pydantic

from mona import context, state


@dataclasses.dataclass
class RequestBodyIsNotReceivedError(Exception):
    """Request body is None and cannot be taken."""

    message = "Request body is None and cannot be taken."
    code = 400

    def __init__(self):
        """Request body is None and cannot be taken."""


@dataclasses.dataclass
class TypeIsNotDataclassError(Exception):
    """Passed type is not dataclass."""

    def __init__(self, t: typing.Type):
        """Passed type is not dataclass.

        Args:
            t (Type): passed type
        """
        self.message = f"Type {t} is not dataclass."
        self.code = 500


@dataclasses.dataclass
class TypeIsNotPydanticBaseModelError(Exception):
    """Passed type is not `pydantic.BaseModel`."""

    def __init__(self, t: typing.Type):
        """Passed type is not `pydantic.BaseModel`.

        Args:
            t (Type): passed type
        """
        self.message = f"Type {t} is not pydantic BaseModel."
        self.code = 500


def take_body(ctx: context.Context) -> state.ESafe[bytes]:
    """Take request body as byte string."""
    if ctx.request.body is None:
        return state.Error(RequestBodyIsNotReceivedError())

    return state.Right(ctx.request.body)


def take_body_as_dict(ctx: context.Context) -> state.ESafe[dict]:
    """Take request body as dict."""
    if ctx.request.body is None:
        return state.Error(RequestBodyIsNotReceivedError())

    return state.Right(orjson.loads(ctx.request.body))


def take_body_as_dataclass(
    dataclass_type: typing.Type,
) -> typing.Callable[[context.Context], state.ESafe[object]]:
    """Take request body as dataclass."""
    # This exception can be raised as this is higher order function that will be
    # executed at app construction stage
    if not dataclasses.is_dataclass(dataclass_type):
        raise TypeIsNotDataclassError(dataclass_type)

    def _handler(ctx: context.Context) -> dataclass_type:
        if ctx.request.body is None:
            return state.Error(RequestBodyIsNotReceivedError())

        return state.Right(dataclass_type(**orjson.loads(ctx.request.body)))

    return _handler


def take_body_as_pydantic(
    model_type: typing.Type[pydantic.BaseModel],
) -> typing.Callable[[context.Context], state.ESafe[pydantic.BaseModel]]:
    """Take request body as pydantic BaseModel."""
    # This exception can be raised as this is higher order function that will be
    # executed at app construction stage
    if not issubclass(model_type, pydantic.BaseModel):
        raise TypeIsNotPydanticBaseModelError(model_type)

    def _handler(ctx: context.Context) -> state.ESafe[model_type]:
        if ctx.request.body is None:
            return state.Error(RequestBodyIsNotReceivedError())

        return state.Right(model_type.parse_raw(ctx.request.body))

    return _handler


def take_body_as_str(ctx: context.Context) -> state.ESafe[str]:
    """Take request body as str."""
    if ctx.request.body is None:
        return state.Error(RequestBodyIsNotReceivedError())

    return state.Right(ctx.request.body.decode("UTF-8"))
