# Response Status

> Auto-generated documentation for [moona.http.response_status](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Response Status
    - [accepted](#accepted)
    - [bad_gateway](#bad_gateway)
    - [bad_request](#bad_request)
    - [conflict](#conflict)
    - [created](#created)
    - [forbidden](#forbidden)
    - [gateway_timeout](#gateway_timeout)
    - [gone](#gone)
    - [http_version_not_supported](#http_version_not_supported)
    - [im_a_teapot](#im_a_teapot)
    - [internal_server_error](#internal_server_error)
    - [method_not_allowed](#method_not_allowed)
    - [no_content](#no_content)
    - [not_acceptable](#not_acceptable)
    - [not_found](#not_found)
    - [not_implemented](#not_implemented)
    - [ok](#ok)
    - [precondition_required](#precondition_required)
    - [service_unavailable](#service_unavailable)
    - [set_accepted](#set_accepted)
    - [set_bad_gateway](#set_bad_gateway)
    - [set_bad_request](#set_bad_request)
    - [set_conflict](#set_conflict)
    - [set_created](#set_created)
    - [set_forbidden](#set_forbidden)
    - [set_gateway_timeout](#set_gateway_timeout)
    - [set_gone](#set_gone)
    - [set_http_version_not_supported](#set_http_version_not_supported)
    - [set_im_a_teapot](#set_im_a_teapot)
    - [set_internal_server_error](#set_internal_server_error)
    - [set_method_not_allowed](#set_method_not_allowed)
    - [set_no_content](#set_no_content)
    - [set_not_acceptable](#set_not_acceptable)
    - [set_not_found](#set_not_found)
    - [set_not_implemented](#set_not_implemented)
    - [set_ok](#set_ok)
    - [set_precondition_required](#set_precondition_required)
    - [set_service_unavailable](#set_service_unavailable)
    - [set_status](#set_status)
    - [set_too_many_requests](#set_too_many_requests)
    - [set_unauthorized](#set_unauthorized)
    - [set_unprocessable_entity](#set_unprocessable_entity)
    - [set_unsupported_media_type](#set_unsupported_media_type)
    - [too_many_requests](#too_many_requests)
    - [unauthorized](#unauthorized)
    - [unprocessable_entity](#unprocessable_entity)
    - [unsupported_media_type](#unsupported_media_type)

## accepted

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L362)

```python
def accepted(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code ACCEPTED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## bad_gateway

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L517)

```python
def bad_gateway(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code BAD_GATEWAY and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## bad_request

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L382)

```python
def bad_request(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code BAD_REQUEST and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## conflict

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L436)

```python
def conflict(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code CONFLICT and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## created

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L353)

```python
def created(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code CREATED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## forbidden

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L400)

```python
def forbidden(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code FORBIDDEN and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## gateway_timeout

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L535)

```python
def gateway_timeout(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code GATEWAY_TIMEOUT and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## gone

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L445)

```python
def gone(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code GONE and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## http_version_not_supported

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L544)

```python
def http_version_not_supported(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code HTTP_VERSION_NOT_SUPPORTED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## im_a_teapot

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L463)

```python
def im_a_teapot(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code IM_A_TEAPOT and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## internal_server_error

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L499)

```python
def internal_server_error(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code INTERNAL_SERVER_ERROR and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## method_not_allowed

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L418)

```python
def method_not_allowed(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code METHOD_NOT_ALLOWED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## no_content

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L371)

```python
@handler
def no_content(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Sets status code NO_CONTENT and respond with passed data.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## not_acceptable

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L427)

```python
def not_acceptable(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code NOT_ACCEPTABLE and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## not_found

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L409)

```python
def not_found(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code NOT_FOUND and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## not_implemented

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L508)

```python
def not_implemented(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code NOT_IMPLEMENTED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## ok

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L344)

```python
def ok(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code OK and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## precondition_required

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L481)

```python
def precondition_required(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code PRECONDITION_REQUIRED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## service_unavailable

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L526)

```python
def service_unavailable(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code SERVICE_UNAVAILABLE and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## set_accepted

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L97)

```python
@handler
def set_accepted(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to ACCEPTED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_bad_gateway

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L296)

```python
@handler
def set_bad_gateway(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to BAD_GATEWAY.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_bad_request

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L119)

```python
@handler
def set_bad_request(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to BAD_REQUEST.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_conflict

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L187)

```python
@handler
def set_conflict(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to CONFLICT.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_created

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L86)

```python
@handler
def set_created(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to CREATED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_forbidden

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L141)

```python
@handler
def set_forbidden(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to FORBIDDEN.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_gateway_timeout

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L320)

```python
@handler
def set_gateway_timeout(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to GATEWAY_TIMEOUT.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_gone

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L198)

```python
@handler
def set_gone(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Sets response status code to GONE.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_http_version_not_supported

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L331)

```python
@handler
def set_http_version_not_supported(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to HTTP_VERSION_NOT_SUPPORTED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_im_a_teapot

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L222)

```python
@handler
def set_im_a_teapot(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to IM_A_TEAPOT.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_internal_server_error

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L272)

```python
@handler
def set_internal_server_error(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to INTERNAL_SERVER_ERROR.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_method_not_allowed

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L163)

```python
@handler
def set_method_not_allowed(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to METHOD_NOT_ALLOWED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_no_content

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L108)

```python
@handler
def set_no_content(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to NO_CONTENT.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_not_acceptable

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L176)

```python
@handler
def set_not_acceptable(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to NOT_ACCEPTABLE.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_not_found

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L152)

```python
@handler
def set_not_found(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to NOT_FOUND.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_not_implemented

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L285)

```python
@handler
def set_not_implemented(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to NOT_IMPLEMENTED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_ok

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L75)

```python
@handler
def set_ok(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Sets response status code to OK.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_precondition_required

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L246)

```python
@handler
def set_precondition_required(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to PRECONDITION_REQUIRED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_service_unavailable

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L307)

```python
@handler
def set_service_unavailable(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to SERVICE_UNAVAILABLE.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_status

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L67)

```python
@handler1
def set_status(
    code: int,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Set response status to `code`.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)

## set_too_many_requests

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L259)

```python
@handler
def set_too_many_requests(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to TOO_MANY_REQUESTS.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_unauthorized

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L130)

```python
@handler
def set_unauthorized(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to UNAUTHORIZED.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_unprocessable_entity

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L233)

```python
@handler
def set_unprocessable_entity(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to UNPROCESSABLE_ENTITY.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## set_unsupported_media_type

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L209)

```python
@handler
def set_unsupported_media_type(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response status code to UNSUPPORTED_MEDIA_TYPE.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## too_many_requests

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L490)

```python
def too_many_requests(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code TOO_MANY_REQUESTS and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## unauthorized

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L391)

```python
def unauthorized(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code UNAUTHORIZED and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## unprocessable_entity

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L472)

```python
def unprocessable_entity(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code UNPROCESSABLE_ENTITY and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## unsupported_media_type

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_status.py#L454)

```python
def unsupported_media_type(data: bytes | str | BaseModel) -> HTTPHandler:
```

Sets status code UNSUPPORTED_MEDIA_TYPE and respond with passed data.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)
