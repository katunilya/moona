from typing import Any, Callable

import pytest
from pydantic import BaseModel

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPHandler, end
from moona.http.request_body import bind_dict, bind_int, bind_model, bind_raw, bind_text


def check_for(result) -> Callable[[Any], HTTPHandler]:
    def _check_for(data) -> HTTPHandler:
        assert data == result
        return lambda _, ctx: end(ctx)

    return _check_for


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, binder, handler",
    [
        (b"", bind_raw, check_for(b"")),
        (b"Hello, World!!!", bind_raw, check_for(b"Hello, World!!!")),
        (b"Goodbye, World!!!", bind_raw, check_for(b"Goodbye, World!!!")),
        (b"", bind_text, check_for("")),
        (b"Hello, World!!!", bind_text, check_for("Hello, World!!!")),
        (b"Goodbye, World!!!", bind_text, check_for("Goodbye, World!!!")),
        (b"0", bind_int, check_for(0)),
        (b"-1", bind_int, check_for(-1)),
        (b"1", bind_int, check_for(1)),
        (
            b'{"name": "John Doe", "age": 33}',
            bind_dict,
            check_for({"name": "John Doe", "age": 33}),
        ),
        (
            b'{"name":"John Doe","age": 33}',
            bind_dict,
            check_for({"name": "John Doe", "age": 33}),
        ),
        (
            b'{\n    "name": "John Doe",\n    "age": 33\n}',
            bind_dict,
            check_for({"name": "John Doe", "age": 33}),
        ),
    ],
)
async def test_body_bind(ctx: HTTPContext, request_body, binder, handler):
    ctx.received = True
    ctx.request_body = request_body
    await binder(handler)(end, ctx)


class TestBaseModel(BaseModel):  # noqa
    name: str
    age: int


test = TestBaseModel(name="John Doe", age=33)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model, request_body, handler",
    [
        (TestBaseModel, b'{"name": "John Doe", "age": 33}', check_for(test)),
        (TestBaseModel, b'{"name":"John Doe","age": 33}', check_for(test)),
        (
            TestBaseModel,
            b'{\n    "name": "John Doe",\n    "age": 33\n}',
            check_for(test),
        ),
    ],
)
async def test_bind_model(ctx: HTTPContext, model, request_body, handler):
    ctx.received = True
    ctx.request_body = request_body
    await bind_model(model, handler)(end, ctx)
