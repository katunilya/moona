from typing import TypeVar

import orjson
from pydantic import BaseModel
from pymon import Future, Pipe

from moona.http.context import HTTPContext, set_response_body
from moona.http.events import send_body
from moona.http.handlers import HTTPFunc, HTTPHandler, handler1
from moona.http.header import set_content_type
from moona.utils import encode_utf_8

TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


@handler1
def set_bytes(
    data: bytes, nxt: HTTPFunc, ctx: HTTPContext
) -> Future[HTTPContext | None]:
    """Sets response body to passed `bytes`.

    Args:
        data (bytes): body.
        nxt (HTTPFunc): next func to run.
        ctx (HTTPContext): to set body to.
    """
    return Pipe(ctx) << set_response_body(data) >> nxt


def set_text(data: str) -> HTTPHandler:
    """Sets response body to passed `str`.

    Data is converted to `bytes` under the hood. "Content-Type: text/plain" header is
    also set.

    Args:
        data (str): body.
    """
    return (Pipe(data).then(encode_utf_8).then(set_bytes).finish()) >> set_content_type(
        "text/plain"
    )


def set_json(data: TBaseModel) -> HTTPHandler:
    """Sets response body to passed pydantic `BaseModel` as json `bytes` sequence.

    Also sets "Content-Type: application/json" header.

    Args:
        data (TBaseModel): body_
    """
    return (
        Pipe(data).then(BaseModel.dict).then(orjson.dumps).then(set_bytes).finish()
    ) >> set_content_type("application/json")


def send_bytes(data: str) -> HTTPHandler:
    """Sets response body to passed `bytes` and sends them.

    Args:
        data (str): body.
    """
    return set_bytes(data) >> send_body


def send_text(data: str) -> HTTPHandler:
    """Sets response body to passed `str` and sends text/plain response.

    Args:
        data (str): body as text/plain.
    """
    return set_text(data) >> send_body


def send_json(data: TBaseModel) -> HTTPHandler:
    """Sets response body to passed `BaseModel` and send application/json response.

    Args:
        data (TBaseModel): body as application/json.
    """
    return set_json(data) >> send_body
