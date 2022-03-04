from mona import context

CONTINUE: int = 100
SWITCHING_PROTOCOLS: int = 101
PROCESSING: int = 102
EARLY: int = 103

OK: int = 200
CREATED: int = 201
ACCEPTED: int = 202
NON_AUTHORITATIVE_INFORMATION: int = 203
NO_CONTENT: int = 204
RESET_CONTENT: int = 205
PARTIAL_CONTENT: int = 206
MULTI_STATUS: int = 207
IM_USED: int = 226

MULTIPLE_CHOICES: int = 300
MOVED_PERMANENTLY: int = 301
FOUND: int = 302
SEE_OTHER: int = 303
NOT_MODIFIED: int = 304
USE_PROXY: int = 305
UNUSED: int = 306
TEMPORARY_REDIRECT: int = 307
PERMANENT_REDIRECT: int = 308

BAD_REQUEST: int = 400
UNAUTHORIZED: int = 401
PAYMENT_REQUIRED: int = 402
FORBIDDEN: int = 403
NOT_FOUND: int = 404
METHOD_NOT_ALLOWED: int = 405
NOT_ACCEPTABLE: int = 406
PROXY_AUTHENTICATION_REQUIRED: int = 407
REQUEST_TIMEOUT: int = 408
CONFLICT: int = 409
GONE: int = 410
LENGTH_REQUIRED: int = 411
PRECONDITION_FAILED: int = 412
PAYLOAD_TO_LARGE: int = 413
URI_TOO_LONG: int = 414
UNSUPPORTED_MEDIA_TYPE: int = 415
RANGE_NOT_SATISFIABLE: int = 416
EXPECTATION_FAILED: int = 417
UNPROCESSABLE_ENTITY: int = 422
LOCKED: int = 423
FAILED_DEPENDENCY: int = 424
UPGRADE_REQUIRED: int = 426
PRECONDITION_REQUIRED: int = 428
TOO_MANY_REQUESTS: int = 429
REQUEST_HEADER_FIELDS_TOO_LARGE: int = 431

INTERNAL_SERVER_ERROR: int = 500
NOT_IMPLEMENTED: int = 501
BAD_GATEWAY: int = 502
SERVICE_UNAVAILABLE: int = 503
GATEWAY_TIMEOUT: int = 504
HTTP_VERSION_NOT_SUPPORTED: int = 505
INSUFFICIENT_STORAGE: int = 507
NOT_EXTENDED: int = 510
NETWORK_AUTHENTICATION_REQUIRED: int = 511


def set_status(code: int) -> context.Handler:
    """Generates handler that sets passed status code into response status code."""

    def _handler(context: context.Context) -> context.Context:
        context.response_status = code
        return context

    return _handler


def set_status_ok(ctx: context.Context) -> context.Context:
    """Sets status code 200 to response."""
    return set_status(OK)(ctx)


def set_status_created(ctx: context.Context) -> context.Context:
    """Sets status code 201 to response."""
    return set_status(CREATED)(ctx)


def set_status_bad_request(ctx: context.Context) -> context.Context:
    """Sets status code 400 to response."""
    return set_status(BAD_REQUEST)(ctx)


def set_status_unauthorized(ctx: context.Context) -> context.Context:
    """Sets status code 401 to response."""
    return set_status(UNAUTHORIZED)(ctx)


def set_status_forbidden(ctx: context.Context) -> context.Context:
    """Sets status code 403 to response."""
    return set_status(FORBIDDEN)(ctx)


def set_status_not_found(ctx: context.Context) -> context.Context:
    """Sets status code 404 to response."""
    return set_status(NOT_FOUND)(ctx)


def set_status_method_not_allowed(ctx: context.Context) -> context.Context:
    """Sets status code 405 to response."""
    return set_status(METHOD_NOT_ALLOWED)(ctx)


def set_status_internal_server_error(ctx: context.Context) -> context.Context:
    """Sets status code 500 to response."""
    return set_status(INTERNAL_SERVER_ERROR)(ctx)


def set_status_not_implemented(ctx: context.Context) -> context.Context:
    """Sets status code 501 to response."""
    return set_status(NOT_IMPLEMENTED)(ctx)


def set_status_bad_gateway(ctx: context.Context) -> context.Context:
    """Sets status code 502 to response."""
    return set_status(BAD_GATEWAY)(ctx)
