from fundom import future, pipe
from pydantic import BaseModel

from moona.http.context import HTTPContext, set_response_status
from moona.http.handlers import HTTPFunc, HTTPHandler, handler, handler1
from moona.http.response_body import negotiate, raw

CONTINUE = 100
SWITCHING_PROTOCOLS = 101
EARLY_HINTS = 103

OK = 200
CREATED = 201
ACCEPTED = 202
NON_AUTHORITATIVE_INFORMATION = 203
NO_CONTENT = 204
RESET_CONTENT = 205
PARTIAL_CONTENT = 206

MULTIPLE_CHOICES = 300
MOVED_PERMANENTLY = 301
FOUND = 302
SEE_OTHER = 303
NOT_MODIFIED = 304
TEMPORARY_REDIRECT = 307
PERMANENT_REDIRECT = 308

BAD_REQUEST = 400
UNAUTHORIZED = 401
PAYMENT_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
NOT_ACCEPTABLE = 406
PROXY_AUTHENTICATION_REQUIRED = 407
REQUEST_TIMEOUT = 408
CONFLICT = 409
GONE = 410
LENGTH_REQUIRED = 411
PRECONDITION_FAILED = 412
PAYLOAD_TOO_LARGE = 413
URI_TOO_LONG = 414
UNSUPPORTED_MEDIA_TYPE = 415
RANGE_NOT_SATISFIABLE = 416
EXPECTATION_FAILED = 417
IM_A_TEAPOT = 418
UNPROCESSABLE_ENTITY = 422
TOO_EARLY = 425
UPGRADE_REQUIRED = 426
PRECONDITION_REQUIRED = 428
TOO_MANY_REQUESTS = 429
REQUEST_HEADER_FIELDS_TOO_LARGE = 431
UNAVAILABLE_FOR_LEGAL_REASONS = 451

INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED = 501
BAD_GATEWAY = 502
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
HTTP_VERSION_NOT_SUPPORTED = 505
VARIANT_ALSO_NEGOTIATES = 506
INSUFFICIENT_STORAGE = 507
LOOP_DETECTED = 508
NOT_EXTENDED = 510


@handler1
def set_status(
    code: int, nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Set response status to `code`."""
    return pipe(ctx) << set_response_status(code) >> nxt


@handler
def set_ok(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to OK.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(OK)(nxt, ctx)


@handler
def set_created(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to CREATED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(CREATED)(nxt, ctx)


@handler
def set_accepted(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to ACCEPTED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(ACCEPTED)(nxt, ctx)


@handler
def set_no_content(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to NO_CONTENT.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(NO_CONTENT)(nxt, ctx)


@handler
def set_bad_request(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to BAD_REQUEST.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(BAD_REQUEST)(nxt, ctx)


@handler
def set_unauthorized(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to UNAUTHORIZED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(UNAUTHORIZED)(nxt, ctx)


@handler
def set_forbidden(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to FORBIDDEN.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(FORBIDDEN)(nxt, ctx)


@handler
def set_not_found(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to NOT_FOUND.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(NOT_FOUND)(nxt, ctx)


@handler
def set_method_not_allowed(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to METHOD_NOT_ALLOWED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(METHOD_NOT_ALLOWED)(nxt, ctx)


@handler
def set_not_acceptable(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to NOT_ACCEPTABLE.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(NOT_ACCEPTABLE)(nxt, ctx)


@handler
def set_conflict(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to CONFLICT.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(CONFLICT)(nxt, ctx)


@handler
def set_gone(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to GONE.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(GONE)(nxt, ctx)


@handler
def set_unsupported_media_type(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to UNSUPPORTED_MEDIA_TYPE.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(UNSUPPORTED_MEDIA_TYPE)(nxt, ctx)


@handler
def set_im_a_teapot(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to IM_A_TEAPOT.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(IM_A_TEAPOT)(nxt, ctx)


@handler
def set_unprocessable_entity(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to UNPROCESSABLE_ENTITY.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(UNPROCESSABLE_ENTITY)(nxt, ctx)


@handler
def set_precondition_required(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to PRECONDITION_REQUIRED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(PRECONDITION_REQUIRED)(nxt, ctx)


@handler
def set_too_many_requests(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to TOO_MANY_REQUESTS.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(TOO_MANY_REQUESTS)(nxt, ctx)


@handler
def set_internal_server_error(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to INTERNAL_SERVER_ERROR.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(INTERNAL_SERVER_ERROR)(nxt, ctx)


@handler
def set_not_implemented(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to NOT_IMPLEMENTED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(NOT_IMPLEMENTED)(nxt, ctx)


@handler
def set_bad_gateway(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to BAD_GATEWAY.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(BAD_GATEWAY)(nxt, ctx)


@handler
def set_service_unavailable(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to SERVICE_UNAVAILABLE.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(SERVICE_UNAVAILABLE)(nxt, ctx)


@handler
def set_gateway_timeout(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets response status code to GATEWAY_TIMEOUT.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(GATEWAY_TIMEOUT)(nxt, ctx)


@handler
def set_http_version_not_supported(
    nxt: HTTPFunc, ctx: HTTPContext
) -> future[HTTPContext | None]:
    """Sets response status code to HTTP_VERSION_NOT_SUPPORTED.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return set_status(HTTP_VERSION_NOT_SUPPORTED)(nxt, ctx)


def ok(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code OK and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_ok >> negotiate(data)


def created(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code CREATED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_created >> negotiate(data)


def accepted(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code ACCEPTED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_accepted >> negotiate(data)


@handler
def no_content(nxt: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
    """Sets status code NO_CONTENT and respond with passed data.

    Args:
        nxt (HTTPFunc): to run next.
        ctx (HTTPContext): to process.
    """
    return (set_no_content >> raw(b""))(nxt, ctx)


def bad_request(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code BAD_REQUEST and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_bad_request >> negotiate(data)


def unauthorized(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code UNAUTHORIZED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_unauthorized >> negotiate(data)


def forbidden(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code FORBIDDEN and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_forbidden >> negotiate(data)


def not_found(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code NOT_FOUND and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_not_found >> negotiate(data)


def method_not_allowed(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code METHOD_NOT_ALLOWED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_method_not_allowed >> negotiate(data)


def not_acceptable(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code NOT_ACCEPTABLE and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_not_acceptable >> negotiate(data)


def conflict(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code CONFLICT and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_conflict >> negotiate(data)


def gone(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code GONE and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_gone >> negotiate(data)


def unsupported_media_type(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code UNSUPPORTED_MEDIA_TYPE and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_unsupported_media_type >> negotiate(data)


def im_a_teapot(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code IM_A_TEAPOT and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_im_a_teapot >> negotiate(data)


def unprocessable_entity(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code UNPROCESSABLE_ENTITY and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_unprocessable_entity >> negotiate(data)


def precondition_required(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code PRECONDITION_REQUIRED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_precondition_required >> negotiate(data)


def too_many_requests(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code TOO_MANY_REQUESTS and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_too_many_requests >> negotiate(data)


def internal_server_error(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code INTERNAL_SERVER_ERROR and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_internal_server_error >> negotiate(data)


def not_implemented(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code NOT_IMPLEMENTED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_not_implemented >> negotiate(data)


def bad_gateway(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code BAD_GATEWAY and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_bad_gateway >> negotiate(data)


def service_unavailable(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code SERVICE_UNAVAILABLE and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_service_unavailable >> negotiate(data)


def gateway_timeout(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code GATEWAY_TIMEOUT and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_gateway_timeout >> negotiate(data)


def http_version_not_supported(data: bytes | str | BaseModel) -> HTTPHandler:
    """Sets status code HTTP_VERSION_NOT_SUPPORTED and respond with passed data.

    Args:
        data (bytes | str | BaseModel): to respond with.
    """
    return set_http_version_not_supported >> negotiate(data)
