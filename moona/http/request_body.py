from logging.handlers import HTTPHandler
from typing import Callable, Type, TypeVar

import orjson
from pydantic import BaseModel
from pymon import Future, Pipe

from moona.http.context import HTTPContext, get_request_body
from moona.http.events import receive
from moona.http.handlers import HTTPFunc, handler


def _decode_bytes(data: bytes) -> str:
    return data.decode("UTF-8")


def bind_raw(func: Callable[[bytes], HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on request body.

    Args:
        func (Callable[[bytes], HTTPHandler]): to run on request body.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        handle = (Pipe(ctx) << get_request_body << func).finish()
        return handle(nxt, ctx)

    return receive >> _handler


def bind_text(func: Callable[[str], HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on request body.

    Args:
        func (Callable[[str], HTTPHandler]): to run on request body.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        handle = (Pipe(ctx) << get_request_body << _decode_bytes << func).finish()
        return handle(nxt, ctx)

    return receive >> _handler


def bind_int(func: Callable[[int], HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on request body.

    Args:
        func (Callable[[int], HTTPHandler]): to run on request body.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        handle = (
            Pipe(ctx) << get_request_body << _decode_bytes << int << func
        ).finish()
        return handle(nxt, ctx)

    return receive >> _handler


def bind_dict(func: Callable[[dict], HTTPHandler]) -> HTTPHandler:
    """Executes passed `func` on request body.

    Args:
        func (Callable[[dict], HTTPHandler]): to run on request body.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        handle = (Pipe(ctx) << get_request_body << orjson.loads << func).finish()
        return handle(nxt, ctx)

    return receive >> _handler


TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


def bind_model(
    model: Type[TBaseModel],
    func: Callable[[TBaseModel], HTTPHandler],
) -> HTTPHandler:
    """Executes passed `func` on request body.

    Args:
        model (Type[TBaseModel]): pydantic `BaseModel` to parse to.
        func (Callable[[TBaseModel], HTTPHandler]): to run on request body.
    """

    @handler
    def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
        handle = (
            Pipe(ctx) << get_request_body << orjson.loads << model.parse_obj << func
        ).finish()
        return handle(nxt, ctx)

    return receive >> _handler
