import pytest

from moona.http.context import HTTPContext
from moona.http.handlers import end
from moona.http.request_method import (
    CONNECT,
    DELETE,
    GET,
    HEAD,
    OPTIONS,
    PATCH,
    POST,
    PUT,
    TRACE,
    method,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_method, check_method, result",
    [
        ("GET", "GET", True),
        ("POST", "GET", False),
        ("PATCH", "GET", False),
        ("PUT", "GET", False),
        ("DELETE", "GET", False),
        ("OPTIONS", "GET", False),
        ("HEAD", "GET", False),
        ("TRACE", "GET", False),
        ("CONNECT", "GET", False),
        ("GET", "POST", False),
        ("POST", "POST", True),
        ("PATCH", "POST", False),
        ("PUT", "POST", False),
        ("DELETE", "POST", False),
        ("OPTIONS", "POST", False),
        ("HEAD", "POST", False),
        ("TRACE", "POST", False),
        ("CONNECT", "POST", False),
        ("GET", "PATCH", False),
        ("POST", "PATCH", False),
        ("PATCH", "PATCH", True),
        ("PUT", "PATCH", False),
        ("DELETE", "PATCH", False),
        ("OPTIONS", "PATCH", False),
        ("HEAD", "PATCH", False),
        ("TRACE", "PATCH", False),
        ("CONNECT", "PATCH", False),
        ("GET", "PUT", False),
        ("POST", "PUT", False),
        ("PATCH", "PUT", False),
        ("PUT", "PUT", True),
        ("DELETE", "PUT", False),
        ("OPTIONS", "PUT", False),
        ("HEAD", "PUT", False),
        ("TRACE", "PUT", False),
        ("CONNECT", "PUT", False),
        ("GET", "DELETE", False),
        ("POST", "DELETE", False),
        ("PATCH", "DELETE", False),
        ("PUT", "DELETE", False),
        ("DELETE", "DELETE", True),
        ("OPTIONS", "DELETE", False),
        ("HEAD", "DELETE", False),
        ("TRACE", "DELETE", False),
        ("CONNECT", "DELETE", False),
        ("GET", "OPTIONS", False),
        ("POST", "OPTIONS", False),
        ("PATCH", "OPTIONS", False),
        ("PUT", "OPTIONS", False),
        ("DELETE", "OPTIONS", False),
        ("OPTIONS", "OPTIONS", True),
        ("HEAD", "OPTIONS", False),
        ("TRACE", "OPTIONS", False),
        ("CONNECT", "OPTIONS", False),
        ("GET", "HEAD", False),
        ("POST", "HEAD", False),
        ("PATCH", "HEAD", False),
        ("PUT", "HEAD", False),
        ("DELETE", "HEAD", False),
        ("OPTIONS", "HEAD", False),
        ("HEAD", "HEAD", True),
        ("TRACE", "HEAD", False),
        ("CONNECT", "HEAD", False),
        ("GET", "TRACE", False),
        ("POST", "TRACE", False),
        ("PATCH", "TRACE", False),
        ("PUT", "TRACE", False),
        ("DELETE", "TRACE", False),
        ("OPTIONS", "TRACE", False),
        ("HEAD", "TRACE", False),
        ("TRACE", "TRACE", True),
        ("CONNECT", "TRACE", False),
        ("GET", "CONNECT", False),
        ("POST", "CONNECT", False),
        ("PATCH", "CONNECT", False),
        ("PUT", "CONNECT", False),
        ("DELETE", "CONNECT", False),
        ("OPTIONS", "CONNECT", False),
        ("HEAD", "CONNECT", False),
        ("TRACE", "CONNECT", False),
        ("CONNECT", "CONNECT", True),
    ],
)
async def test_method(ctx: HTTPContext, request_method, check_method, result):
    ctx.request_method = request_method
    _ctx = await method(check_method)(end, ctx)
    assert (_ctx is not None) == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_method, method_handler, result",
    [
        ("GET", GET, True),
        ("POST", GET, False),
        ("PATCH", GET, False),
        ("PUT", GET, False),
        ("DELETE", GET, False),
        ("OPTIONS", GET, False),
        ("HEAD", GET, False),
        ("TRACE", GET, False),
        ("CONNECT", GET, False),
        ("GET", POST, False),
        ("POST", POST, True),
        ("PATCH", POST, False),
        ("PUT", POST, False),
        ("DELETE", POST, False),
        ("OPTIONS", POST, False),
        ("HEAD", POST, False),
        ("TRACE", POST, False),
        ("CONNECT", POST, False),
        ("GET", PATCH, False),
        ("POST", PATCH, False),
        ("PATCH", PATCH, True),
        ("PUT", PATCH, False),
        ("DELETE", PATCH, False),
        ("OPTIONS", PATCH, False),
        ("HEAD", PATCH, False),
        ("TRACE", PATCH, False),
        ("CONNECT", PATCH, False),
        ("GET", PUT, False),
        ("POST", PUT, False),
        ("PATCH", PUT, False),
        ("PUT", PUT, True),
        ("DELETE", PUT, False),
        ("OPTIONS", PUT, False),
        ("HEAD", PUT, False),
        ("TRACE", PUT, False),
        ("CONNECT", PUT, False),
        ("GET", DELETE, False),
        ("POST", DELETE, False),
        ("PATCH", DELETE, False),
        ("PUT", DELETE, False),
        ("DELETE", DELETE, True),
        ("OPTIONS", DELETE, False),
        ("HEAD", DELETE, False),
        ("TRACE", DELETE, False),
        ("CONNECT", DELETE, False),
        ("GET", OPTIONS, False),
        ("POST", OPTIONS, False),
        ("PATCH", OPTIONS, False),
        ("PUT", OPTIONS, False),
        ("DELETE", OPTIONS, False),
        ("OPTIONS", OPTIONS, True),
        ("HEAD", OPTIONS, False),
        ("TRACE", OPTIONS, False),
        ("CONNECT", OPTIONS, False),
        ("GET", HEAD, False),
        ("POST", HEAD, False),
        ("PATCH", HEAD, False),
        ("PUT", HEAD, False),
        ("DELETE", HEAD, False),
        ("OPTIONS", HEAD, False),
        ("HEAD", HEAD, True),
        ("TRACE", HEAD, False),
        ("CONNECT", HEAD, False),
        ("GET", TRACE, False),
        ("POST", TRACE, False),
        ("PATCH", TRACE, False),
        ("PUT", TRACE, False),
        ("DELETE", TRACE, False),
        ("OPTIONS", TRACE, False),
        ("HEAD", TRACE, False),
        ("TRACE", TRACE, True),
        ("CONNECT", TRACE, False),
        ("GET", CONNECT, False),
        ("POST", CONNECT, False),
        ("PATCH", CONNECT, False),
        ("PUT", CONNECT, False),
        ("DELETE", CONNECT, False),
        ("OPTIONS", CONNECT, False),
        ("HEAD", CONNECT, False),
        ("TRACE", CONNECT, False),
        ("CONNECT", CONNECT, True),
    ],
)
async def test_concrete_method(
    ctx: HTTPContext, request_method, method_handler, result
):
    ctx.request_method = request_method
    _ctx = await method_handler(end, ctx)
    assert (_ctx is not None) == result
