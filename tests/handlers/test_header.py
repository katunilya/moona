import pytest

from mona.core import HTTPContext
from mona.handlers.header import get_header, remove_header, set_header
from mona.monads.maybe import Maybe
from mona.monads.result import Result


@pytest.mark.parametrize(
    "name, value, result_name, result_value",
    [
        ("Content-Type", "text/plain", b"content-type", b"text/plain"),
        ("Content-Length", "30", b"content-length", b"30"),
        ("Content-Type", "application/json", b"content-type", b"application/json"),
    ],
)
def test_set_header(ctx: HTTPContext, name, value, result_name, result_value):
    result = set_header(name, value)(Result.successfull(ctx))
    assert result.value.response.headers[result_name] == result_value


def test_remove_header(ctx: HTTPContext):
    ctx.response.headers[b"content-type"] = b"application/json"
    result = remove_header("Content-Type")(Result.successfull(ctx))
    assert result.value.response.headers.get(b"content-type", None) is None


def test_get_header(ctx: HTTPContext):
    ctx.request.headers[b"content-type"] = b"application/json"
    assert get_header("Content-Type")(ctx) == Maybe.some(
        ("content-type", "application/json")
    )
