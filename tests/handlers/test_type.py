from mona.core import HTTPContext
from mona.handlers.type import http


def test_reqest_on_type(ctx: HTTPContext):
    assert isinstance(ctx >> http, HTTPContext)
