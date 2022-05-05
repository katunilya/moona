from typing import Callable, Type, TypeVar

import orjson
import toolz
from pydantic import BaseModel

from mona.core import ContextError, HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, compose, do, http_handler
from mona.handlers.events import receive_body_async, send_body_async
from mona.handlers.header import set_header
from mona.monads.future import Future
from mona.monads.result import Failure, Result, Safe, Success
from mona.utils import decode_utf_8, deserialize, encode_utf_8

T = TypeVar("T")


def get_body_bytes_async(ctx: HTTPContext) -> Future[Safe[bytes]]:
    """Try to get `HTTPRequest` body as raw `bytes`.

    If request body was not received than it will be. Than it will be extracted as
    `Safe` from `HTTPContext`. Due to asynchronous nature of `receive_body` result is
    some `Future`.

    Args:
        ctx (HTTPContext): to try to get body from.

    Returns:
        Future[Safe[bytes]]: async result.
    """
    return do(
        ctx,
        receive_body_async,
        Result.safely_bound(lambda ctx_: ctx_.request.body),
    )


def get_body_text_async(ctx: HTTPContext) -> Future[Safe[str]]:
    """Try to get `HTTPRequest` body as `str`.

    Gets body as `bytes` first and than decode as UTF-8.

    Args:
        ctx (HTTPContext): to try to get body from.

    Returns:
        Future[Safe[str]]: async result.
    """
    return do(
        ctx,
        receive_body_async,
        Result.safely_bound(decode_utf_8),
    )


def get_body_json_async(
    target_type: Type[BaseModel],
) -> Callable[[HTTPContext], Future[Safe[BaseModel]]]:
    """Parses `bytes` body as JSON to passed type and returns that from context.

    Powered by `pydantic` `BaseModel`.

    Notes:
        * https://pydantic-docs.helpmanual.io/

    Args:
        target_type (Type[BaseModel]): to deserialize to.

    Returns:
        Callable[[HTTPContext], Future[Safe[BaseModel]]]: body getter.
    """

    def _get_json_body(ctx: HTTPContext) -> Future[Safe[BaseModel]]:
        return do(
            ctx,
            get_body_bytes_async,
            Result.safely_bound(deserialize(target_type)),
        )

    return _get_json_body


def set_body_bytes(data: bytes) -> HTTPHandler:
    """`HTTPContext` handler that sets passed `bytes` to `HTTPResponse` body.

    Also sets headers:
    * Content-Length: XXX

    Args:
        data (bytes): to set as response body.
    """
    set_content_length = set_header("Content-Length", str(len(data)))

    @http_handler
    def _set_body_bytes(ctx: HTTPContext) -> HTTPContextResult:
        ctx.response.body = data
        return ctx >> set_content_length

    return _set_body_bytes


def set_body_text(data: str) -> HTTPHandler:
    """`HTTPContext` handler that sets passed `str` to `HTTPResponse` body.

    Also sets headers:
    * Content-Type: text/plain
    * Content-Length: XXX

    Args:
        data (str): to set as response body.
    """
    return toolz.compose_left(
        set_body_bytes(encode_utf_8(data)),
        set_header("Content-Type", "text/plain"),
    )


def set_body_json(data: BaseModel) -> HTTPHandler:
    """`HTTPHandler` that sets passed `BaseModel` as json body of `HTTPResponse`.

    Also sets headers:
    * Content-Type: application/json
    * Content-Length: XXX

    Args:
        data (BaseModel): to set as response body.
    """
    return toolz.compose_left(
        set_body_bytes(orjson.dumps(data.dict())),
        set_header("Content-Type", "application/json"),
    )


def bind_body_bytes_async(
    func: Callable[[HTTPContext], Future[Safe[bytes]]]
) -> HTTPHandler:
    """`HTTPHandler` that sets `bytes` processed from `func` execution.

    Args:
        func (Callable[[HTTPContext], Future[Safe[bytes]]]): sync or async func that
        produces error-safe `bytes`.
    """

    @http_handler
    async def _bind_body_bytes(ctx: HTTPContext) -> HTTPContextResult:
        result: Safe[bytes] = await (Future.create(ctx) >> func)

        match result:
            case Success(data):
                return ctx >> set_body_bytes(data)
            case Failure(err):
                return ContextError(ctx, str(err))

    return _bind_body_bytes


def bind_body_text_async(
    func: Callable[[HTTPContext], Future[Safe[str]]]
) -> HTTPHandler:
    """`HTTPHandler` that sets `str` processed from `func` execution.

    Args:
        func (Callable[[HTTPContext], Future[Safe[str]]]): sync or async func that
        produces error-safe `str`.
    """

    @http_handler
    async def _bind_body_text(ctx: HTTPContext) -> HTTPContextResult:
        result: Safe[str] = await (Future.create(ctx) >> func)

        match result:
            case Success(data):
                return ctx >> set_body_text(data)
            case Failure(err):
                return ContextError(ctx, str(err))

    return _bind_body_text


def bind_body_json_async(
    func: Callable[[HTTPContext], Future[Safe[BaseModel]]]
) -> HTTPHandler:
    """`HTTPHandler` that sets `BaseModel` processed from `func` execution.

    Args:
        func (Callable[[HTTPContext], Future[Safe[BaseModel]]]): sync or async func that
        produces error-safe `BaseModel`.
    """

    @http_handler
    async def _bind_body_json(ctx: HTTPContext) -> HTTPContextResult:
        result: Safe[BaseModel] = await (Future.create(ctx) >> func)

        match result:
            case Success(data):
                return ctx >> set_body_json(data)
            case Failure(err):
                return ContextError(ctx, str(err))

    return _bind_body_json


def send_body_bytes_async(data: bytes) -> HTTPHandler:
    """`HTTPHandler` that sets body to passed `bytes` and sends the response.

    Also sets headers:
    * Content-Length: XXX

    Args:
        data (bytes): to set as response body.
    """
    return compose(
        set_body_bytes(data),
        send_body_async,
    )


def send_body_text_async(data: str) -> HTTPHandler:
    """`HTTPHandler` that sets body to passed `str` and sends the response.

    Also sets headers:
    * Content-Type: text/plain
    * Content-Length: XXX

    Args:
        data (str): to set as response body.
    """
    return compose(
        set_body_text(data),
        send_body_async,
    )


def send_body_json_async(data: BaseModel) -> HTTPHandler:
    """`HTTPHandler` that sets body to passed `BaseModel` as json and sends response.

    Also sets headers:
    * Content-Type: application/json
    * Content-Length: XXX

    Args:
        data (BaseModel): to set as response body.
    """
    return compose(
        set_body_json(data),
        send_body_async,
    )
