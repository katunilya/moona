import pytest

from moona.http import HTTPContext, end
from moona.http.handlers import HTTPHandler
from moona.http.response_status import (
    ACCEPTED,
    BAD_GATEWAY,
    BAD_REQUEST,
    CONFLICT,
    CREATED,
    FORBIDDEN,
    GATEWAY_TIMEOUT,
    GONE,
    HTTP_VERSION_NOT_SUPPORTED,
    IM_A_TEAPOT,
    INTERNAL_SERVER_ERROR,
    METHOD_NOT_ALLOWED,
    NO_CONTENT,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    NOT_IMPLEMENTED,
    OK,
    PRECONDITION_REQUIRED,
    SERVICE_UNAVAILABLE,
    TOO_MANY_REQUESTS,
    UNAUTHORIZED,
    UNPROCESSABLE_ENTITY,
    UNSUPPORTED_MEDIA_TYPE,
    no_content,
    set_accepted,
    set_bad_gateway,
    set_bad_request,
    set_conflict,
    set_created,
    set_forbidden,
    set_gateway_timeout,
    set_gone,
    set_http_version_not_supported,
    set_im_a_teapot,
    set_internal_server_error,
    set_method_not_allowed,
    set_no_content,
    set_not_acceptable,
    set_not_found,
    set_not_implemented,
    set_ok,
    set_precondition_required,
    set_service_unavailable,
    set_status,
    set_too_many_requests,
    set_unauthorized,
    set_unprocessable_entity,
    set_unsupported_media_type,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "code",
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
async def test_set_status(ctx: HTTPContext, code):
    _ctx = await set_status(code)(end, ctx)
    assert _ctx.response_status == code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "handler, code",
    [
        (set_ok, OK),
        (set_created, CREATED),
        (set_accepted, ACCEPTED),
        (set_no_content, NO_CONTENT),
        (set_bad_request, BAD_REQUEST),
        (set_unauthorized, UNAUTHORIZED),
        (set_forbidden, FORBIDDEN),
        (set_not_found, NOT_FOUND),
        (set_method_not_allowed, METHOD_NOT_ALLOWED),
        (set_not_acceptable, NOT_ACCEPTABLE),
        (set_conflict, CONFLICT),
        (set_gone, GONE),
        (set_unsupported_media_type, UNSUPPORTED_MEDIA_TYPE),
        (set_im_a_teapot, IM_A_TEAPOT),
        (set_unprocessable_entity, UNPROCESSABLE_ENTITY),
        (set_precondition_required, PRECONDITION_REQUIRED),
        (set_too_many_requests, TOO_MANY_REQUESTS),
        (set_internal_server_error, INTERNAL_SERVER_ERROR),
        (set_not_implemented, NOT_IMPLEMENTED),
        (set_bad_gateway, BAD_GATEWAY),
        (set_service_unavailable, SERVICE_UNAVAILABLE),
        (set_gateway_timeout, GATEWAY_TIMEOUT),
        (set_http_version_not_supported, HTTP_VERSION_NOT_SUPPORTED),
    ],
)
async def test_status_handlers(ctx: HTTPContext, handler: HTTPHandler, code):
    _ctx = await handler(end, ctx)
    assert _ctx.response_status == code


@pytest.mark.asyncio
async def test_no_content(ctx: HTTPContext):
    _ctx = await no_content(end, ctx)
    assert _ctx.response_status == NO_CONTENT
    assert _ctx.response_body == b""
