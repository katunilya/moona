from typing import Any, Callable

import pytest
from pydantic import BaseModel

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPHandler, end
from moona.http.response_body import negotiate, set_json, set_raw, set_text


class TestInnerBaseModel(BaseModel):  # noqa
    address: str
    phone: str


class TestBaseModel(BaseModel):  # noqa
    name: str
    age: int
    info: TestInnerBaseModel


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setter, data, result",
    [
        (set_raw, b"", b""),
        (set_raw, b"Hello, World!!!", b"Hello, World!!!"),
        (set_raw, b"Goodbye, World!!!", b"Goodbye, World!!!"),
        (set_text, "", b""),
        (set_text, "Hello, World!!!", b"Hello, World!!!"),
        (set_text, "Goodbye, World!!!", b"Goodbye, World!!!"),
        (
            set_json,
            TestBaseModel(
                name="John Doe",
                age=33,
                info=TestInnerBaseModel(address="NYC", phone="111-11-11"),
            ),
            b'{"name":"John Doe","age":33,"info":{"address":"NYC","phone":"111-11-11"}}',  # noqa
        ),
        (negotiate, b"", b""),
        (negotiate, b"Hello, World!!!", b"Hello, World!!!"),
        (negotiate, b"Goodbye, World!!!", b"Goodbye, World!!!"),
        (negotiate, "", b""),
        (negotiate, "Hello, World!!!", b"Hello, World!!!"),
        (negotiate, "Goodbye, World!!!", b"Goodbye, World!!!"),
        (
            negotiate,
            TestBaseModel(
                name="John Doe",
                age=33,
                info=TestInnerBaseModel(address="NYC", phone="111-11-11"),
            ),
            b'{"name":"John Doe","age":33,"info":{"address":"NYC","phone":"111-11-11"}}',  # noqa
        ),
    ],
)
async def test_setters(
    ctx: HTTPContext, setter: Callable[[Any], HTTPHandler], data, result
):
    _ctx = await setter(data)(end, ctx)
    assert _ctx.response_body == result
