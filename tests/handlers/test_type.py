import pytest

from mona.core import HTTPContext
from mona.handlers.type import WrongRequestType, http


@pytest.mark.parametrize(
    "type_, assert_result",
    [
        ("http", HTTPContext),
        ("websocket", WrongRequestType),
    ],
)
def test_reqest_on_type(ctx: HTTPContext, type_, assert_result):
    ctx.request.type_ = type_
    assert isinstance(ctx >> http, assert_result)
