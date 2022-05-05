from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler

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


def set_status(code: int) -> HTTPHandler:
    """`HTTPHandler` that sets status code to response."""

    @http_handler
    def _status(ctx: HTTPContext) -> HTTPContext:
        ctx.response.status = code
        return ctx

    return _status


__set_status_ok = set_status(OK)
__set_status_created = set_status(CREATED)
__set_status_bad_request = set_status(BAD_REQUEST)
__set_status_unauthorized = set_status(UNAUTHORIZED)
__set_status_forbidden = set_status(FORBIDDEN)
__set_status_not_found = set_status(NOT_FOUND)
__set_status_method_not_allowed = set_status(METHOD_NOT_ALLOWED)
__set_status_internal_server_error = set_status(INTERNAL_SERVER_ERROR)
__set_status_not_implemented = set_status(NOT_IMPLEMENTED)
__set_status_bad_gateway = set_status(BAD_GATEWAY)


@http_handler
def set_status_ok(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to OK."""
    return __set_status_ok(ctx)


@http_handler
def set_status_created(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to CREATED."""
    return __set_status_created(ctx)


@http_handler
def set_status_bad_request(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to BAD_REQUEST."""
    return __set_status_bad_request(ctx)


@http_handler
def set_status_unauthorized(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to UNAUTHORIZED."""
    return __set_status_unauthorized(ctx)


@http_handler
def set_status_forbidden(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to FORBIDDEN."""
    return __set_status_forbidden(ctx)


@http_handler
def set_status_not_found(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to NOT_FOUND."""
    return __set_status_not_found(ctx)


@http_handler
def set_status_method_not_allowed(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to METHOD_NOT_ALLOWED."""
    return __set_status_method_not_allowed(ctx)


@http_handler
def set_status_internal_server_error(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to INTERNAL_SERVER_ERROR."""
    return __set_status_internal_server_error(ctx)


@http_handler
def set_status_not_implemented(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to NOT_IMPLEMENTED."""
    return __set_status_not_implemented(ctx)


@http_handler
def set_status_bad_gateway(ctx: HTTPContext) -> HTTPContextResult:
    """Handler that sets `HTTPResponse` status to BAD_GATEWAY."""
    return __set_status_bad_gateway(ctx)
