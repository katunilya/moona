import pytest

from mona.core import HTTPContext
from mona.handlers.type import http
from mona.monads import Failure, Success


@pytest.mark.parametrize(
    "type_, initial, assert_result",
    [
        ("http", Success, Success),
        ("websocket", Success, Failure),
        ("http", Failure, Failure),
        ("websocket", Failure, Failure),
    ],
)
def test_reqest_on_type(ctx: HTTPContext, type_, initial, assert_result):
    ctx.request.type_ = type_
    result = http(initial(ctx))
    assert isinstance(result, assert_result)
