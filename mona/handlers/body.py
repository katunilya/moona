from dataclasses import is_dataclass
from typing import Any, Awaitable, Callable, Type, TypeVar

import orjson
from pydantic import BaseModel

from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, compose, http_handler
from mona.handlers.error import HTTPContextError
from mona.handlers.header import set_header
from mona.monads.future import Future
from mona.monads.maybe import Maybe, Nothing, Some
from mona.monads.result import Failure, Result, Success
from mona.utils import encode_utf_8, serialize


class BodyNotReceivedError(HTTPContextError):
    """Request body was not received, but attempted to be accessed."""

    def __init__(
        self,
        ctx: HTTPContext,
    ) -> None:
        super().__init__(
            ctx,
            "Internal Server Error: Attempt to get Request body failed as body was not "
            "received.",
            500,
        )


class BodyIsNotValidJson(HTTPContextError):
    """Request body cannot be parsed as json."""

    def __init__(self, ctx: HTTPContext, err: Exception) -> None:
        super().__init__(
            ctx, f"Internal Server Error: Request body is not valid json.\n{err}", 500
        )


def set_body_bytes(body: bytes) -> HTTPHandler:
    """`HTTPContext` handler that sets passed `bytes` to `HTTPResponse` body.

    Based on the length of body sets "Content-Length" response header.
    """
    content_length = len(body)

    @http_handler
    def _set_body_bytes(ctx: HTTPContext) -> HTTPContextResult:
        ctx.response.body = body
        return Success(ctx) >> set_header("Content-Length", content_length)

    return _set_body_bytes


def set_body_text(body: str) -> HTTPHandler:
    """`HTTPContext` handler that sets passed `str` to `HTTPResponse` body.

    Body is encoded as UTF-8. "Content-Type: text/plain" header is set.
    """
    body: str = body.encode("UTF-8")

    @http_handler
    def _set_body_text(ctx: HTTPContext) -> HTTPContextResult:
        return (
            Success(ctx)
            >> set_body_bytes(body)
            >> set_header("Content-Type", "text/plain")
        )

    return _set_body_text


def set_body_json(body: object) -> HTTPHandler:
    """`HTTPContext` handler that serializes passed object to JSON.

    Users `orjson` as it is the fastest JSON serializer/deserializer. Supports all types
    that `orjson` supports and `pydantic` `BaseModel`. In case object cannot be
    serialized exception on stage of handler build is raised. It is acceptable due to
    evaluation of `HTTPHandler` not at runtime.

    Also sets header "Content-Type: application/json" and "Content-Length: ..."

    Note:
        * https://github.com/ijl/orjson#serialize
    """
    match body:
        case BaseModel() as base_model:
            json_body: bytes = orjson.dumps(base_model.dict())
        case other:
            json_body: bytes = orjson.dumps(other)

    @http_handler
    def _set_body_json(ctx: HTTPContext) -> HTTPContextResult:
        return (
            Success(ctx)
            >> set_body_bytes(json_body)
            >> set_header("Content-Type", "application/json")
        )

    return _set_body_json


def set_body_bytes_from(
    func: Callable[
        [HTTPContext], Result[bytes, Exception] | Awaitable[Result[bytes, Exception]]
    ]
) -> HTTPHandler:
    """`HTTPContext` handler that sets body from `bytes` result of some func."""

    @http_handler
    async def _set_body_bytes_from(ctx: HTTPContext) -> HTTPContextResult:
        match await (Future.create(ctx) >> func):
            case Failure() as failure:
                return Failure(HTTPContextError(ctx, str(failure.value)))
            case body:
                return Success(ctx) >> set_body_bytes(body)

    return _set_body_bytes_from


def set_body_str_from(
    func: Callable[
        [HTTPContext], Result[str, Exception] | Awaitable[Result[str, Exception]]
    ]
) -> HTTPHandler:
    """`HTTPContext` handler that sets body from `str` result of some func.

    Also sets header "Content-Type: text/plain".
    """
    return compose(
        set_body_bytes_from(
            compose(
                func,
                Result.bound(encode_utf_8),
            )
        ),
        set_header("Content-Type", "text/plain"),
    )


def set_body_json_from(
    func: Callable[
        [HTTPContext], Result[object, Exception] | Awaitable[Result[object, Exception]]
    ]
) -> HTTPHandler:
    """`HTTPContext` handler that sets body from some object converted to `json`."""
    return compose(
        set_body_bytes_from(
            compose(
                func,
                Result.bound(serialize),
            )
        ),
        set_header("Content-Type", "application/json"),
    )


def get_body_bytes(
    ctx: HTTPContext,
) -> Result[Maybe[bytes], BodyNotReceivedError]:
    """Try to get `HTTPRequest` body as raw `bytes`.

    Args:
        ctx (HTTPContext): to try to get body from.

    Returns:
        Result[Maybe[bytes], BodyNotReceivedError]: If body was not received, than
        `Failure` is returned. If body is empty than `Success`full `Nothing` is
        returned. Otherwise `Some` body is returned.
    """
    match ctx.request.body:
        case None:
            return Failure(BodyNotReceivedError(ctx))
        case b"":
            return Success(Nothing())
        case not_empty_body:
            return Success(Some(not_empty_body))


def get_body_str(ctx: HTTPContext) -> Result[Maybe[str], BodyNotReceivedError]:
    """Try to get `HTTPRequest` body as `str`.

    Args:
        ctx (HTTPContext): to try to get body from.

    Returns:
        Result[Maybe[str], BodyNotReceivedError]: If body was not received, than
        `Failure` is returned. If body is empty than `Success`full `Nothing` is
        returned. Otherwise `Some` body is returned.
    """
    match ctx.request.body:
        case None:
            return Failure(BodyNotReceivedError(ctx))
        case b"":
            return Success(Nothing())
        case not_empty_body:
            return Success(Some(not_empty_body.decode("UTF-8")))


def get_body_json_dict(
    ctx: HTTPContext,
) -> Result[Maybe[dict], BodyNotReceivedError | BodyIsNotValidJson]:
    """Try to get `HTTPRequest` body as json and map to Python `dict`.

    Args:
        ctx (HTTPContext): to try to get body from.

    Returns:
        Result[Maybe[dict], BodyNotReceivedError | BodyIsNotValidJson]: If body is not
        received than `Failure[BodyNotReceivedError]` returned. If body is empty `bytes`
        than `Success[Nothing]` is returned. If body is not empty, but cannot be mapped
        as json to Python `dict` than `Failure[BodyIsNotValidJson]` is returned.
        Otherwise `Success[dict]` is returned.
    """
    match ctx.request.body:
        case None:
            return Failure(BodyNotReceivedError(ctx))
        case b"":
            return Success(Nothing())
        case not_empty_body:
            try:
                return Success(Some(orjson.loads(not_empty_body)))
            except orjson.JSONDecodeError as err:
                return Failure(BodyIsNotValidJson(ctx, err))


def get_body_json_dataclass(
    dataclass_type: Type,
) -> Callable[
    [HTTPContext], Result[Maybe[object], BodyNotReceivedError | BodyIsNotValidJson]
]:
    """Try to get `HTTPRequest` body as json and map to some `dataclass`.

    If passed type is not dataclass, than `Exception` will be raised. In this case error
    will be raised during ASGI server composition and exception can be raised directly.

    Args:
        dataclass_type (Type): to map json `bytes` to.

    Returns:
        Callable[[HTTPContext], Result[Maybe[object], BodyNotReceivedError |
        BodyIsNotValidJson]]: function that actually returns result. If body is not
        received than `Failure[BodyNotReceivedError]` returned. If body is empty `bytes`
        than `Success[Nothing]` is returned. If body is not empty, but cannot be mapped
        as json to Python `dict` than `Failure[BodyIsNotValidJson]` is returned.
        Otherwise `Success[object]` is returned.
    """
    if not is_dataclass(dataclass_type):
        raise Exception(f"{dataclass_type} is not dataclass.")

    def _get_body_json_dataclass(
        ctx: HTTPContext,
    ) -> Result[Maybe[object], BodyNotReceivedError | BodyIsNotValidJson]:
        match ctx.request.body:
            case None:
                return Failure(BodyNotReceivedError(ctx))
            case b"":
                return Success(Nothing())
            case not_empty_body:
                try:
                    return Success(Some(dataclass_type(**orjson.loads(not_empty_body))))
                except orjson.JSONDecodeError as err:
                    return Failure(BodyIsNotValidJson(ctx, err))

    return _get_body_json_dataclass


def get_body_json_pydantic(
    pydantic_type: Type[BaseModel],
) -> Callable[
    [HTTPContext], Result[Maybe[BaseModel], BodyNotReceivedError | BodyIsNotValidJson]
]:
    """Try to get `HTTPRequest` body as json and map to some `pydantic` `BaseModel`.

    If passed type is not `pydantic`'s `BaseModel`, than `Exception` will be raised. In
    this case error will be raised during ASGI server composition and exception can be
    raised directly.

    Args:
        pydantic_type (BaseModel): to map json `bytes` to.

    Returns:
        Callable[[HTTPContext], Result[Maybe[BaseModel], BodyNotReceivedError |
        BodyIsNotValidJson]]: function that actually returns result. If body is not
        received than `Failure[BodyNotReceivedError]` returned. If body is empty `bytes`
        than `Success[Nothing]` is returned. If body is not empty, but cannot be mapped
        as json to Python `dict` than `Failure[BodyIsNotValidJson]` is returned.
        Otherwise `Success[BaseModel]` is returned.
    """
    if not issubclass(pydantic_type, BaseModel):
        raise Exception(f"{pydantic_type} is not pydantic BaseModel.")

    def _get_body_json_pydantic(
        ctx: HTTPContext,
    ) -> Result[Maybe[object], BodyNotReceivedError | BodyIsNotValidJson]:
        match ctx.request.body:
            case None:
                return Failure(BodyNotReceivedError(ctx))
            case b"":
                return Success(Nothing())
            case not_empty_body:
                try:
                    return Success(Some(pydantic_type.parse_raw(not_empty_body)))
                except orjson.JSONDecodeError as err:
                    return Failure(BodyIsNotValidJson(ctx, err))

    return _get_body_json_pydantic


def get_body_json(
    type_: Type[Any],
) -> Callable[
    [HTTPContext], Result[Maybe[BaseModel], BodyNotReceivedError | BodyIsNotValidJson]
]:
    """Provides facade for other dict/dataclass/pydantic json body getters.

    Args:
        type_ (Type[Any]): to parse JSON from.

    Returns:
        Callable[ [HTTPContext], Result[Maybe[BaseModel], BodyNotReceivedError |
        BodyIsNotValidJson] ]: resulting JSON body getter function.
    """
    if issubclass(type_, BaseModel):
        return get_body_json_pydantic(type_)

    if is_dataclass(type_):
        return get_body_json_dataclass(type_)

    if type_ == dict:
        return get_body_json_dict

    return lambda ctx: Failure(BodyIsNotValidJson(ctx, f"Wrong type: {type_}"))


T = TypeVar("T")
V = TypeVar("V")


def bind_json(
    request_type: Type[T],
    func: Callable[[T], Awaitable[HTTPHandler] | HTTPHandler],
) -> HTTPHandler:
    """`HTTPHandler` that handles full receive-respond JSON cycle.

    This handler fully processes the response. It closes connection and finishes
    response by itself.

    Args:
        request_type (Type[T]): to what type request JSON body should be bind.

    Returns:
        HTTPHandler: resulting handler that actually performs action.
    """
    return compose(
        set_body_json_from(
            compose(
                get_body_json(request_type),
                func,
            )
        ),
    )
