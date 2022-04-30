from enum import IntEnum

from mona.core import HTTPContext
from mona.handlers.core import HTTPContextResult, HTTPHandler, http_handler
from mona.monads.result import Success


class HTTPStatusCode(IntEnum):
    """Basic HTTP Status codes."""

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


def set_status(code: HTTPStatusCode) -> HTTPHandler:
    """`HTTPHandler` that sets status code to response."""

    @http_handler
    def _status(ctx: HTTPContext) -> HTTPContextResult:
        ctx.response.status = code
        return Success(ctx)

    return _status


set_status_ok = set_status(HTTPStatusCode.OK)
set_status_created = set_status(HTTPStatusCode.CREATED)
set_status_bad_request = set_status(HTTPStatusCode.BAD_REQUEST)
set_status_unauthorized = set_status(HTTPStatusCode.UNAUTHORIZED)
set_status_forbidden = set_status(HTTPStatusCode.FORBIDDEN)
set_status_not_found = set_status(HTTPStatusCode.NOT_FOUND)
set_status_method_not_allowed = set_status(HTTPStatusCode.METHOD_NOT_ALLOWED)
set_status_internal_server_error = set_status(HTTPStatusCode.INTERNAL_SERVER_ERROR)
set_status_not_implemented = set_status(HTTPStatusCode.NOT_IMPLEMENTED)
set_status_bad_gateway = set_status(HTTPStatusCode.BAD_GATEWAY)
