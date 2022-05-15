from pymon import Future, Pipe

from moona.http.context import HTTPContext, set_response_status
from moona.http.handlers import HTTPFunc, handler

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


@handler
def ok(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to 200 OK."""
    return Pipe(ctx) << set_response_status(OK) >> nxt


@handler
def created(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to CREATED."""
    return Pipe(ctx) << set_response_status(CREATED) >> nxt


@handler
def bad_request(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to BAD_REQUEST."""
    return Pipe(ctx) << set_response_status(BAD_REQUEST) >> nxt


@handler
def unauthorized(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to UNAUTHORIZED."""
    return Pipe(ctx) << set_response_status(UNAUTHORIZED) >> nxt


@handler
def forbidden(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to FORBIDDEN."""
    return Pipe(ctx) << set_response_status(FORBIDDEN) >> nxt


@handler
def not_found(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to NOT_FOUND."""
    return Pipe(ctx) << set_response_status(NOT_FOUND) >> nxt


@handler
def method_not_allowed(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to METHOD_NOT_ALLOWED."""
    return Pipe(ctx) << set_response_status(METHOD_NOT_ALLOWED) >> nxt


@handler
def internal_server_error(
    nxt: HTTPFunc, ctx: HTTPContext
) -> Future[HTTPContext | None]:
    """Set response status to INTERNAL_SERVER_ERROR."""
    return Pipe(ctx) << set_response_status(INTERNAL_SERVER_ERROR) >> nxt


@handler
def not_implemented(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to NOT_IMPLEMENTED."""
    return Pipe(ctx) << set_response_status(NOT_IMPLEMENTED) >> nxt


@handler
def bad_gateway(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
    """Set response status to BAD_GATEWAY."""
    return Pipe(ctx) << set_response_status(BAD_GATEWAY) >> nxt
