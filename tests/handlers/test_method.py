import pytest

from moona.context import HTTPContext
from moona.handlers.method import (
    CONNECT,
    DELETE,
    GET,
    HEAD,
    OPTIONS,
    PATCH,
    POST,
    PUT,
    TRACE,
    WrongHTTPMethodError,
    method,
)


@pytest.mark.parametrize(
    "arrange_method, method_, result_type",
    [
        ("GET", "GET", HTTPContext),
        ("POST", "GET", WrongHTTPMethodError),
        ("PATCH", "GET", WrongHTTPMethodError),
        ("PUT", "GET", WrongHTTPMethodError),
        ("DELETE", "GET", WrongHTTPMethodError),
        ("OPTIONS", "GET", WrongHTTPMethodError),
        ("HEAD", "GET", WrongHTTPMethodError),
        ("TRACE", "GET", WrongHTTPMethodError),
        ("CONNECT", "GET", WrongHTTPMethodError),
        ("GET", "POST", WrongHTTPMethodError),
        ("POST", "POST", HTTPContext),
        ("PATCH", "POST", WrongHTTPMethodError),
        ("PUT", "POST", WrongHTTPMethodError),
        ("DELETE", "POST", WrongHTTPMethodError),
        ("OPTIONS", "POST", WrongHTTPMethodError),
        ("HEAD", "POST", WrongHTTPMethodError),
        ("TRACE", "POST", WrongHTTPMethodError),
        ("CONNECT", "POST", WrongHTTPMethodError),
        ("GET", "PATCH", WrongHTTPMethodError),
        ("POST", "PATCH", WrongHTTPMethodError),
        ("PATCH", "PATCH", HTTPContext),
        ("PUT", "PATCH", WrongHTTPMethodError),
        ("DELETE", "PATCH", WrongHTTPMethodError),
        ("OPTIONS", "PATCH", WrongHTTPMethodError),
        ("HEAD", "PATCH", WrongHTTPMethodError),
        ("TRACE", "PATCH", WrongHTTPMethodError),
        ("CONNECT", "PATCH", WrongHTTPMethodError),
        ("GET", "PUT", WrongHTTPMethodError),
        ("POST", "PUT", WrongHTTPMethodError),
        ("PATCH", "PUT", WrongHTTPMethodError),
        ("PUT", "PUT", HTTPContext),
        ("DELETE", "PUT", WrongHTTPMethodError),
        ("OPTIONS", "PUT", WrongHTTPMethodError),
        ("HEAD", "PUT", WrongHTTPMethodError),
        ("TRACE", "PUT", WrongHTTPMethodError),
        ("CONNECT", "PUT", WrongHTTPMethodError),
        ("GET", "DELETE", WrongHTTPMethodError),
        ("POST", "DELETE", WrongHTTPMethodError),
        ("PATCH", "DELETE", WrongHTTPMethodError),
        ("PUT", "DELETE", WrongHTTPMethodError),
        ("DELETE", "DELETE", HTTPContext),
        ("OPTIONS", "DELETE", WrongHTTPMethodError),
        ("HEAD", "DELETE", WrongHTTPMethodError),
        ("TRACE", "DELETE", WrongHTTPMethodError),
        ("CONNECT", "DELETE", WrongHTTPMethodError),
        ("GET", "OPTIONS", WrongHTTPMethodError),
        ("POST", "OPTIONS", WrongHTTPMethodError),
        ("PATCH", "OPTIONS", WrongHTTPMethodError),
        ("PUT", "OPTIONS", WrongHTTPMethodError),
        ("DELETE", "OPTIONS", WrongHTTPMethodError),
        ("OPTIONS", "OPTIONS", HTTPContext),
        ("HEAD", "OPTIONS", WrongHTTPMethodError),
        ("TRACE", "OPTIONS", WrongHTTPMethodError),
        ("CONNECT", "OPTIONS", WrongHTTPMethodError),
        ("GET", "HEAD", WrongHTTPMethodError),
        ("POST", "HEAD", WrongHTTPMethodError),
        ("PATCH", "HEAD", WrongHTTPMethodError),
        ("PUT", "HEAD", WrongHTTPMethodError),
        ("DELETE", "HEAD", WrongHTTPMethodError),
        ("OPTIONS", "HEAD", WrongHTTPMethodError),
        ("HEAD", "HEAD", HTTPContext),
        ("TRACE", "HEAD", WrongHTTPMethodError),
        ("CONNECT", "HEAD", WrongHTTPMethodError),
        ("GET", "TRACE", WrongHTTPMethodError),
        ("POST", "TRACE", WrongHTTPMethodError),
        ("PATCH", "TRACE", WrongHTTPMethodError),
        ("PUT", "TRACE", WrongHTTPMethodError),
        ("DELETE", "TRACE", WrongHTTPMethodError),
        ("OPTIONS", "TRACE", WrongHTTPMethodError),
        ("HEAD", "TRACE", WrongHTTPMethodError),
        ("TRACE", "TRACE", HTTPContext),
        ("CONNECT", "TRACE", WrongHTTPMethodError),
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


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", HTTPContext),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_GET(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> GET, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", HTTPContext),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_POST(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> POST, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", HTTPContext),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_PATCH(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> PATCH, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", HTTPContext),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_PUT(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> PUT, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", HTTPContext),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_DELETE(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> DELETE, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", HTTPContext),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_OPTIONS(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> OPTIONS, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", HTTPContext),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_HEAD(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> HEAD, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", HTTPContext),
        ("CONNECT", WrongHTTPMethodError),
    ],
)
def test_TRACE(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> TRACE, result_type)


@pytest.mark.parametrize(
    "method_, result_type",
    [
        ("GET", WrongHTTPMethodError),
        ("POST", WrongHTTPMethodError),
        ("PATCH", WrongHTTPMethodError),
        ("PUT", WrongHTTPMethodError),
        ("DELETE", WrongHTTPMethodError),
        ("OPTIONS", WrongHTTPMethodError),
        ("HEAD", WrongHTTPMethodError),
        ("TRACE", WrongHTTPMethodError),
        ("CONNECT", HTTPContext),
    ],
)
def test_CONNECT(ctx: HTTPContext, method_, result_type):  # noqa
    ctx.request.method = method_
    assert isinstance(ctx >> CONNECT, result_type)
