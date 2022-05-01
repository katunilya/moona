import pytest
from pydantic import BaseModel

from mona.core import HTTPContext
from mona.handlers.body import (
    bind_body_bytes_async,
    bind_body_json_async,
    bind_body_text_async,
    send_body_bytes_async,
    send_body_json_async,
    send_body_text_async,
    set_body_bytes,
    set_body_json,
    set_body_text,
)
from mona.monads.result import Result


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"Hello, World!",
        b'{"name": "John Doe", "age": 25}',
    ],
)
def test_set_body_bytes(ctx: HTTPContext, data):
    ctx = ctx >> set_body_bytes(data)
    assert ctx.response.body == data
    assert ctx.response.headers[b"content-length"] == str(len(data)).encode("UTF-8")


@pytest.mark.parametrize(
    "data, result_data",
    [
        ("", b""),
        ("Hello, World!", b"Hello, World!"),
        ('{"name": "John Doe", "age": 25}', b'{"name": "John Doe", "age": 25}'),
    ],
)
def test_set_body_text(ctx: HTTPContext, data, result_data):
    ctx = ctx >> set_body_text(data)
    assert ctx.response.body == result_data
    assert ctx.response.headers[b"content-length"] == str(len(data)).encode("UTF-8")
    assert ctx.response.headers[b"content-type"] == b"text/plain"


class User(BaseModel):  # noqa
    name: str
    age: int


def test_set_body_json(ctx: HTTPContext):
    ctx = ctx >> set_body_json(User(name="John Doe", age=33))
    assert ctx.response.body == b'{"name":"John Doe","age":33}'
    assert ctx.response.headers[b"content-length"] == b"28"
    assert ctx.response.headers[b"content-type"] == b"application/json"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"Hello, World!",
        b'{"name": "John Doe", "age": 25}',
    ],
)
async def test_send_body_bytes_async(ctx: HTTPContext, data):
    ctx = await (ctx >> send_body_bytes_async(data))  # Future for chain of handlers
    assert ctx.response.body == data
    assert ctx.response.headers[b"content-length"] == str(len(data)).encode("UTF-8")
    assert ctx.closed is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, result_data",
    [
        ("", b""),
        ("Hello, World!", b"Hello, World!"),
        ('{"name": "John Doe", "age": 25}', b'{"name": "John Doe", "age": 25}'),
    ],
)
async def test_send_body_text_async(ctx: HTTPContext, data, result_data):
    ctx = await (ctx >> send_body_text_async(data))
    assert ctx.response.body == result_data
    assert ctx.response.headers[b"content-length"] == str(len(data)).encode("UTF-8")
    assert ctx.response.headers[b"content-type"] == b"text/plain"
    assert ctx.closed is True


@pytest.mark.asyncio
async def test_send_body_json_async(ctx: HTTPContext):
    ctx = await (ctx >> send_body_json_async(User(name="John Doe", age=33)))
    assert ctx.response.body == b'{"name":"John Doe","age":33}'
    assert ctx.response.headers[b"content-length"] == b"28"
    assert ctx.response.headers[b"content-type"] == b"application/json"
    assert ctx.closed is True


def create_sync_binding(data):
    def sync_binding(ctx: HTTPContext):
        return Result.successfull(data)

    return sync_binding


def create_async_binding(data):
    async def async_binding(ctx: HTTPContext):
        return Result.successfull(data)

    return async_binding


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func, result",
    [
        (create_sync_binding(b""), b""),
        (create_async_binding(b""), b""),
        (create_sync_binding(b"Hello, World!"), b"Hello, World!"),
        (create_async_binding(b"Hello, World!"), b"Hello, World!"),
        (create_sync_binding(b'{"name":"John Doe"}'), b'{"name":"John Doe"}'),
        (create_async_binding(b'{"name":"John Doe"}'), b'{"name":"John Doe"}'),
    ],
)
async def test_bind_body_bytes_async(ctx: HTTPContext, func, result):
    ctx = await (ctx >> bind_body_bytes_async(func))
    assert ctx.response.body == result
    assert ctx.response.headers[b"content-length"] == str(len(result)).encode("UTF-8")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func, result",
    [
        (create_sync_binding(""), b""),
        (create_async_binding(""), b""),
        (create_sync_binding("Hello, World!"), b"Hello, World!"),
        (create_async_binding("Hello, World!"), b"Hello, World!"),
        (create_sync_binding('{"name":"John Doe"}'), b'{"name":"John Doe"}'),
        (create_async_binding('{"name":"John Doe"}'), b'{"name":"John Doe"}'),
    ],
)
async def test_bind_body_text_async(ctx: HTTPContext, func, result):
    ctx = await (ctx >> bind_body_text_async(func))
    assert ctx.response.body == result
    assert ctx.response.headers[b"content-length"] == str(len(result)).encode("UTF-8")
    assert ctx.response.headers[b"content-type"] == b"text/plain"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func, result",
    [
        (
            create_sync_binding(User(name="John Doe", age=33)),
            b'{"name":"John Doe","age":33}',
        ),
        (
            create_async_binding(User(name="John Doe", age=33)),
            b'{"name":"John Doe","age":33}',
        ),
    ],
)
async def test_bind_body_json_async(ctx: HTTPContext, func, result):
    ctx = await (ctx >> bind_body_json_async(func))
    assert ctx.response.body == result
    assert ctx.response.headers[b"content-length"] == str(len(result)).encode("UTF-8")
    assert ctx.response.headers[b"content-type"] == b"application/json"
