from dataclasses import dataclass
from typing import ByteString

import pytest
from pydantic import BaseModel

from mona import context, req


@pytest.mark.parametrize(
    "raw_body,parsed_body",
    [
        (b'{"abc": 3}', {"abc": 3}),
        (b'{"abc": "some_str"}', {"abc": "some_str"}),
        (b"{}", {}),
    ],
)
def test_parse_json_to_dict(
    asgi_context: context.Context, raw_body: ByteString, parsed_body: dict
):
    asgi_context.raw_request_body = raw_body
    ctx = req.parse_json_to_dict(asgi_context)

    assert ctx.request_body == parsed_body


@dataclass
class User:

    name: str
    age: int


@pytest.mark.parametrize(
    "raw_body,parsed_body",
    [
        (b'{"name": "Ilya", "age": 21}', User(name="Ilya", age=21)),
        (b'{"name": "Marina", "age": 23}', User(name="Marina", age=23)),
    ],
)
def test_parse_json_to_dataclass(
    asgi_context: context.Context, raw_body: ByteString, parsed_body: object
):
    asgi_context.raw_request_body = raw_body
    handler_ = req.parse_json_to_dataclass(User)

    ctx: context.Context = handler_(asgi_context)

    assert ctx.request_body == parsed_body


class PydanticUser(BaseModel):

    name: str
    age: int


@pytest.mark.parametrize(
    "raw_body,parsed_body",
    [
        (b'{"name": "Ilya", "age": 21}', PydanticUser(name="Ilya", age=21)),
        (b'{"name": "Marina", "age": 23}', PydanticUser(name="Marina", age=23)),
    ],
)
def test_parse_json_to_pydantic(
    asgi_context: context.Context, raw_body: ByteString, parsed_body: object
):
    asgi_context.raw_request_body = raw_body
    handler_ = req.parse_json_to_pydantic(PydanticUser)

    ctx: context.Context = handler_(asgi_context)

    assert ctx.request_body == parsed_body


@pytest.mark.parametrize(
    "raw_body,parsed_body",
    [
        (b'{"name": "Ilya", "age": 21}', """{"name": "Ilya", "age": 21}"""),
        (b'{"name": "Marina", "age": 23}', """{"name": "Marina", "age": 23}"""),
        (b"", ""),
        (b"Hello, Tests!", "Hello, Tests!"),
    ],
)
def test_parse_to_string(
    asgi_context: context.Context, raw_body: ByteString, parsed_body: str
):
    asgi_context.raw_request_body = raw_body
    ctx = req.parse_to_string(asgi_context)

    assert ctx.request_body == parsed_body
