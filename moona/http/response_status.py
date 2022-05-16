from pymon import Future, Pipe

from moona.http.context import HTTPContext, set_response_status
from moona.http.handlers import HTTPFunc, handler1

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
def set_status(code: int, nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext, None]:
    """Set response status to `code`."""
    return Pipe(ctx) << set_response_status(code) >> nxt


ok = set_status(OK)
created = set_status(CREATED)
accepted = set_status(ACCEPTED)
non_authoritative_information = set_status(NON_AUTHORITATIVE_INFORMATION)
no_content = set_status(NO_CONTENT)
reset_content = set_status(RESET_CONTENT)
partial_content = set_status(PARTIAL_CONTENT)
multiple_choices = set_status(MULTIPLE_CHOICES)
moved_permanently = set_status(MOVED_PERMANENTLY)
found = set_status(FOUND)
see_other = set_status(SEE_OTHER)
not_modified = set_status(NOT_MODIFIED)
temporary_redirect = set_status(TEMPORARY_REDIRECT)
permanent_redirect = set_status(PERMANENT_REDIRECT)
bad_request = set_status(BAD_REQUEST)
unauthorized = set_status(UNAUTHORIZED)
payment_required = set_status(PAYMENT_REQUIRED)
forbidden = set_status(FORBIDDEN)
not_found = set_status(NOT_FOUND)
method_not_allowed = set_status(METHOD_NOT_ALLOWED)
not_acceptable = set_status(NOT_ACCEPTABLE)
proxy_authentication_required = set_status(PROXY_AUTHENTICATION_REQUIRED)
request_timeout = set_status(REQUEST_TIMEOUT)
conflict = set_status(CONFLICT)
gone = set_status(GONE)
length_required = set_status(LENGTH_REQUIRED)
precondition_failed = set_status(PRECONDITION_FAILED)
payload_too_large = set_status(PAYLOAD_TOO_LARGE)
uri_too_long = set_status(URI_TOO_LONG)
unsupported_media_type = set_status(UNSUPPORTED_MEDIA_TYPE)
range_not_satisfiable = set_status(RANGE_NOT_SATISFIABLE)
expectation_failed = set_status(EXPECTATION_FAILED)
im_a_teapot = set_status(IM_A_TEAPOT)
unprocessable_entity = set_status(UNPROCESSABLE_ENTITY)
too_early = set_status(TOO_EARLY)
upgrade_required = set_status(UPGRADE_REQUIRED)
precondition_required = set_status(PRECONDITION_REQUIRED)
too_many_requests = set_status(TOO_MANY_REQUESTS)
request_header_fields_too_large = set_status(REQUEST_HEADER_FIELDS_TOO_LARGE)
unavailable_for_legal_reasons = set_status(UNAVAILABLE_FOR_LEGAL_REASONS)
internal_server_error = set_status(INTERNAL_SERVER_ERROR)
not_implemented = set_status(NOT_IMPLEMENTED)
bad_gateway = set_status(BAD_GATEWAY)
service_unavailable = set_status(SERVICE_UNAVAILABLE)
gateway_timeout = set_status(GATEWAY_TIMEOUT)
http_version_not_supported = set_status(HTTP_VERSION_NOT_SUPPORTED)
variant_also_negotiates = set_status(VARIANT_ALSO_NEGOTIATES)
insufficient_storage = set_status(INSUFFICIENT_STORAGE)
loop_detected = set_status(LOOP_DETECTED)
not_extended = set_status(NOT_EXTENDED)
