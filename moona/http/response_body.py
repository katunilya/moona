import orjson
from fundom import future, pipe
from pydantic import BaseModel

from moona.http.context import HTTPContext, set_response_body
from moona.http.events import respond, start
from moona.http.handlers import HTTPFunc, HTTPHandler, handler1
from moona.http.response_headers import (
    content_type_application_json,
    content_type_text_plain,
)


@handler1
def set_raw(data: bytes, nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response body to passed `bytes`.

    Args:
        data (bytes): body.
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to run on.
    """
    return pipe(ctx) << set_response_body(data) >> nxt


def set_text(data: str) -> HTTPHandler:
    """Sets response body to passed `str`.

    Also sets "Content-Type: text/plain" response header.

    Args:
        data (str): body.
    """
    return set_raw(data.encode("UTF-8")) >> content_type_text_plain


def set_json(data: BaseModel) -> HTTPHandler:
    """Sets response body to passed object json representation.

    Also sets "Content-Type: application/json" response header.

    Args:
        data (BaseModel): body.
    """
    raw = pipe(data) << BaseModel.dict << orjson.dumps
    return set_raw(raw.value) >> content_type_application_json


def raw(data: bytes) -> HTTPHandler:
    """Respond client with raw passed `bytes`.

    Args:
        data (bytes): response body.
    """
    return set_raw(data) >> start >> respond


def text(data: str) -> HTTPHandler:
    """Respond client with passed `str`.

    Also sets "Content-Type: text/plain" response header.

    Args:
        data (str): response body.
    """
    return set_text(data) >> start >> respond


def json(data: BaseModel) -> HTTPHandler:
    """Respond client with passed `BaseModel` json representation.

    Also sets "Content-Type: application/json" response header.

    Args:
        data (BaseModel): response body.
    """
    return set_json(data) >> start >> respond


def negotiate(data: bytes | str | BaseModel) -> HTTPHandler:
    """Respond client with passed data based on its type.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    match data:
        case bytes():
            return raw(data)
        case str():
            return text(data)
        case BaseModel():
            return json(data)
