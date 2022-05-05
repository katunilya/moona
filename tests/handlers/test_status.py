import pytest

from mona.core import HTTPContext
from mona.handlers.status import (
    set_status,
    set_status_bad_gateway,
    set_status_bad_request,
    set_status_created,
    set_status_forbidden,
    set_status_internal_server_error,
    set_status_method_not_allowed,
    set_status_not_found,
    set_status_not_implemented,
    set_status_ok,
    set_status_unauthorized,
)


@pytest.mark.parametrize(
    "status",
    [
        100,
        101,
        103,
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        300,
        301,
        302,
        303,
        304,
        307,
        308,
        400,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        409,
        410,
        411,
        412,
        413,
        414,
        415,
        416,
        417,
        418,
        422,
        425,
        426,
        428,
        429,
        431,
        451,
        500,
        501,
        502,
        503,
        504,
        505,
        506,
        507,
        508,
        510,
    ],
)
def test_set_status(ctx: HTTPContext, status):
    result: HTTPContext = ctx >> set_status(status)
    assert result.response.status == status


@pytest.mark.parametrize(
    "handler, status",
    [
        (set_status_ok, 200),
        (set_status_created, 201),
        (set_status_bad_request, 400),
        (set_status_unauthorized, 401),
        (set_status_forbidden, 403),
        (set_status_not_found, 404),
        (set_status_method_not_allowed, 405),
        (set_status_internal_server_error, 500),
        (set_status_not_implemented, 501),
        (set_status_bad_gateway, 502),
    ],
)
def test_setters(ctx: HTTPContext, handler, status):
    assert (ctx >> handler).response.status == status
