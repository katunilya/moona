from typing import ByteString

import pytest

from mona import context, req


@pytest.mark.parametrize(
    "query_string,result",
    [
        (b"name=John&age=99", {"name": ["John"], "age": ["99"]}),
        (b"users=John&users=Doe", {"users": ["John", "Doe"]}),
    ],
)
def test_parse_query(
    asgi_context: context.Context,
    query_string: ByteString,
    result: dict[str, list[str]],
):
    asgi_context.query_string = query_string

    ctx = req.parse_query(asgi_context)

    assert ctx.query == result
