from mona import context, handler, state

CONTINUE: int = 100
SWITCHING_PROTOCOLS: int = 101
EARLY_HINTS: int = 103

OK: int = 200
CREATED: int = 201
ACCEPTED: int = 202
NON_AUTHORITATIVE_INFORMATION: int = 203
NO_CONTENT: int = 204
RESET_CONTENT: int = 205
PARTIAL_CONTENT: int = 206

MULTIPLE_CHOICES: int = 300
MOVED_PERMANENTLY: int = 301
FOUND: int = 302
SEE_OTHER: int = 303
NOT_MODIFIED: int = 304
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
PAYLOAD_TOO_LARGE: int = 413
URI_TOO_LONG: int = 414
UNSUPPORTED_MEDIA_TYPE: int = 415
RANGE_NOT_SATISFIABLE: int = 416
EXPECTATION_FAILED: int = 417
IM_A_TEAPOT: int = 418
UNPROCESSABLE_ENTITY: int = 422
TOO_EARLY: int = 425
UPGRADE_REQUIRED: int = 426
PRECONDITION_REQUIRED: int = 428
TOO_MANY_REQUESTS: int = 429
REQUEST_HEADER_FIELDS_TOO_LARGE: int = 431
UNAVAILABLE_FOR_LEGAL_REASONS: int = 451

INTERNAL_SERVER_ERROR: int = 500
NOT_IMPLEMENTED: int = 501
BAD_GATEWAY: int = 502
SERVICE_UNAVAILABLE: int = 503
GATEWAY_TIMEOUT: int = 504
HTTP_VERSION_NOT_SUPPORTED: int = 505
VARIANT_ALSO_NEGOTIATES: int = 506
INSUFFICIENT_STORAGE: int = 507
LOOP_DETECTED: int = 508
NOT_EXTENDED: int = 510
NETWORK_AUTHENTICATION_REQUIRED: int = 511


def set_status(code: int) -> handler.Handler:
    """Generates handler that sets passed status code into response status code."""

    @state.accepts_right
    def _handler(ctx: context.Context) -> context.StateContext:
        ctx.response.status = code
        return state.right(ctx)

    return _handler


set_status_ok = set_status(OK)
set_status_created = set_status(CREATED)
set_status_bad_request = set_status(BAD_REQUEST)
set_status_unauthorized = set_status(UNAUTHORIZED)
set_status_forbidden = set_status(FORBIDDEN)
set_status_not_found = set_status(NOT_FOUND)
set_status_method_not_allowed = set_status(METHOD_NOT_ALLOWED)
set_status_internal_server_error = set_status(INTERNAL_SERVER_ERROR)
set_status_not_implemented = set_status(NOT_IMPLEMENTED)
set_status_bad_gateway = set_status(BAD_GATEWAY)
