from typing import Callable, Type, TypeVar

import orjson
from pydantic import BaseModel

from mona.http.core import HTTPContext, HTTPContextHandler, get_request_body, handler
from mona.monads.func import Func
from mona.monads.maybe import Maybe, Nothing, if_not_empty
from mona.monads.pipe import Pipeline
from mona.monads.result import Result
from mona.utils import decode_utf_8, encode_utf_8

from .header import set_content_length, set_content_type_json, set_content_type_text

TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


@handler
def get_request_body_text(ctx: HTTPContext) -> Maybe[str]:
    """Extract response body and convert that to UTF-8 str.

    Args:
        ctx (HTTPContext): to extract from.

    Returns:
        Maybe[str]: `Some` if body received and not
    """
    return (
        Pipeline(ctx)
        .then(get_request_body)
        .then_maybe(if_not_empty)
        .then(Result.excepts(decode_utf_8))
        .then(Result.if_error(Pipeline.this(Nothing())))
        .then(Result.unpack)
    )


def get_request_body_json(
    model: Type[TBaseModel],
) -> Callable[[HTTPContext], Maybe[TBaseModel]]:
    """Exctract response body as json parsed to pydantic `BaseModel`.

    Args:
        model (Type[TBaseModel]): target type.
    """

    @handler
    def _handler(ctx: HTTPContext) -> Maybe[TBaseModel]:
        return (
            Pipeline(ctx)
            .then(get_request_body)
            .then_maybe(if_not_empty)
            .then(Result.excepts(model.parse_raw))
            .then(Result.if_error(Pipeline.this(Nothing())))
            .then(Result.unpack)
        )

    return _handler


def set_response_body(data: bytes) -> HTTPContextHandler:
    """Sets response body to passed `bytes` sequence.

    Args:
        data (bytes): response body.
    """

    @handler
    def _handler(ctx: HTTPContext) -> HTTPContext:
        ctx.response_body = data
        return ctx

    return _handler


def set_response_body_text(data: str) -> HTTPContextHandler:
    """Sets response body to passed `str`.

    Internally converted to `bytes`.

    Also sets headers:
    * Content-Type: text/plain
    * Content-Length: XXX

    Args:
        data (str): response body.
    """
    bytes_data = encode_utf_8(data)
    return (
        Func(set_response_body(bytes_data))
        .then(set_content_type_text)
        .then(set_content_length(len(bytes_data)))
    )


def set_response_body_json(model: TBaseModel) -> HTTPContextHandler:
    """Sets response body to passed `BaseModel`.

    Internally converted to json `bytes`.

    Args:
        model (TBaseModel): response body.
    """
    bytes_data = Pipeline(model).then(BaseModel.dict).then(orjson.dumps).finish()
    return (
        Func(set_response_body(bytes_data))
        .then(set_content_type_json)
        .then(set_content_length(len(bytes_data)))
    )
