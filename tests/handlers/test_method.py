import pytest

from mona.core import HTTPContext
from mona.handlers.method import WrongHTTPMethodError, method


@pytest.mark.parametrize(
    "arrange_method, method_, result_type",
    [
        # GET
        ("GET", "GET", HTTPContext),
        ("POST", "GET", WrongHTTPMethodError),
        ("PATCH", "GET", WrongHTTPMethodError),
        ("PUT", "GET", WrongHTTPMethodError),
        ("DELETE", "GET", WrongHTTPMethodError),
        ("OPTIONS", "GET", WrongHTTPMethodError),
        ("HEAD", "GET", WrongHTTPMethodError),
        ("TRACE", "GET", WrongHTTPMethodError),
        ("CONNECT", "GET", WrongHTTPMethodError),
        # POST
        ("GET", "POST", WrongHTTPMethodError),
        ("POST", "POST", HTTPContext),
        ("PATCH", "POST", WrongHTTPMethodError),
        ("PUT", "POST", WrongHTTPMethodError),
        ("DELETE", "POST", WrongHTTPMethodError),
        ("OPTIONS", "POST", WrongHTTPMethodError),
        ("HEAD", "POST", WrongHTTPMethodError),
        ("TRACE", "POST", WrongHTTPMethodError),
        ("CONNECT", "POST", WrongHTTPMethodError),
        # PATCH
        ("GET", "PATCH", WrongHTTPMethodError),
        ("POST", "PATCH", WrongHTTPMethodError),
        ("PATCH", "PATCH", HTTPContext),
        ("PUT", "PATCH", WrongHTTPMethodError),
        ("DELETE", "PATCH", WrongHTTPMethodError),
        ("OPTIONS", "PATCH", WrongHTTPMethodError),
        ("HEAD", "PATCH", WrongHTTPMethodError),
        ("TRACE", "PATCH", WrongHTTPMethodError),
        ("CONNECT", "PATCH", WrongHTTPMethodError),
        # PUT
        ("GET", "PUT", WrongHTTPMethodError),
        ("POST", "PUT", WrongHTTPMethodError),
        ("PATCH", "PUT", WrongHTTPMethodError),
        ("PUT", "PUT", HTTPContext),
        ("DELETE", "PUT", WrongHTTPMethodError),
        ("OPTIONS", "PUT", WrongHTTPMethodError),
        ("HEAD", "PUT", WrongHTTPMethodError),
        ("TRACE", "PUT", WrongHTTPMethodError),
        ("CONNECT", "PUT", WrongHTTPMethodError),
        # DELETE
        ("GET", "DELETE", WrongHTTPMethodError),
        ("POST", "DELETE", WrongHTTPMethodError),
        ("PATCH", "DELETE", WrongHTTPMethodError),
        ("PUT", "DELETE", WrongHTTPMethodError),
        ("DELETE", "DELETE", HTTPContext),
        ("OPTIONS", "DELETE", WrongHTTPMethodError),
        ("HEAD", "DELETE", WrongHTTPMethodError),
        ("TRACE", "DELETE", WrongHTTPMethodError),
        ("CONNECT", "DELETE", WrongHTTPMethodError),
        # OPTIONS
        ("GET", "OPTIONS", WrongHTTPMethodError),
        ("POST", "OPTIONS", WrongHTTPMethodError),
        ("PATCH", "OPTIONS", WrongHTTPMethodError),
        ("PUT", "OPTIONS", WrongHTTPMethodError),
        ("DELETE", "OPTIONS", WrongHTTPMethodError),
        ("OPTIONS", "OPTIONS", HTTPContext),
        ("HEAD", "OPTIONS", WrongHTTPMethodError),
        ("TRACE", "OPTIONS", WrongHTTPMethodError),
        ("CONNECT", "OPTIONS", WrongHTTPMethodError),
        # HEAD
        ("GET", "HEAD", WrongHTTPMethodError),
        ("POST", "HEAD", WrongHTTPMethodError),
        ("PATCH", "HEAD", WrongHTTPMethodError),
        ("PUT", "HEAD", WrongHTTPMethodError),
        ("DELETE", "HEAD", WrongHTTPMethodError),
        ("OPTIONS", "HEAD", WrongHTTPMethodError),
        ("HEAD", "HEAD", HTTPContext),
        ("TRACE", "HEAD", WrongHTTPMethodError),
        ("CONNECT", "HEAD", WrongHTTPMethodError),
        # TRACE
        ("GET", "TRACE", WrongHTTPMethodError),
        ("POST", "TRACE", WrongHTTPMethodError),
        ("PATCH", "TRACE", WrongHTTPMethodError),
        ("PUT", "TRACE", WrongHTTPMethodError),
        ("DELETE", "TRACE", WrongHTTPMethodError),
        ("OPTIONS", "TRACE", WrongHTTPMethodError),
        ("HEAD", "TRACE", WrongHTTPMethodError),
        ("TRACE", "TRACE", HTTPContext),
        ("CONNECT", "TRACE", WrongHTTPMethodError),
        # CONNECT
        ("GET", "CONNECT", WrongHTTPMethodError),
        ("POST", "CONNECT", WrongHTTPMethodError),
        ("PATCH", "CONNECT", WrongHTTPMethodError),
        ("PUT", "CONNECT", WrongHTTPMethodError),
        ("DELETE", "CONNECT", WrongHTTPMethodError),
        ("OPTIONS", "CONNECT", WrongHTTPMethodError),
        ("HEAD", "CONNECT", WrongHTTPMethodError),
        ("TRACE", "CONNECT", WrongHTTPMethodError),
        ("CONNECT", "CONNECT", HTTPContext),
    ],
)
def test_method(ctx: HTTPContext, arrange_method, method_, result_type):
    ctx.request.method = arrange_method
    assert isinstance(ctx >> method(method_), result_type)
