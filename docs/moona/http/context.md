# Context

> Auto-generated documentation for [moona.http.context](https://github.com/katunilya/moona/blob/main/moona/http/context.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Context
    - [HTTPContext](#httpcontext)
    - [get_asgi_spec_version](#get_asgi_spec_version)
    - [get_asgi_version](#get_asgi_version)
    - [get_client](#get_client)
    - [get_closed](#get_closed)
    - [get_http_version](#get_http_version)
    - [get_received](#get_received)
    - [get_request_body](#get_request_body)
    - [get_request_headers](#get_request_headers)
    - [get_request_method](#get_request_method)
    - [get_request_path](#get_request_path)
    - [get_request_query_string](#get_request_query_string)
    - [get_response_body](#get_response_body)
    - [get_response_headers](#get_response_headers)
    - [get_response_status](#get_response_status)
    - [get_scheme](#get_scheme)
    - [get_scope_type](#get_scope_type)
    - [get_server](#get_server)
    - [get_started](#get_started)
    - [send_message](#send_message)
    - [set_closed](#set_closed)
    - [set_received](#set_received)
    - [set_response_body](#set_response_body)
    - [set_response_header](#set_response_header)
    - [set_response_status](#set_response_status)
    - [set_started](#set_started)

## HTTPContext

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L18)

```python
dataclass(slots=True)
class HTTPContext(BaseContext):
    def __init__(scope: Scope, receive: Receive, send: Send) -> None:
```

Object that contains entire information related to HTTP Request.

Mostly it's structure is replication of HTTP Connection Scope of ASGI Specification.
It contains information on both request and response and also functions for sending
and receiving information.

#### Notes

https://asgi.readthedocs.io/en/latest/specs/www.html#

#### See also

- [BaseContext](../context.md#basecontext)
- [Receive](../context.md#receive)
- [Scope](../context.md#scope)
- [Send](../context.md#send)

## get_asgi_spec_version

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L198)

```python
def get_asgi_spec_version(ctx: HTTPContext):
```

Returns `HTTPContext.asgi_spec_version`.

#### See also

- [HTTPContext](#httpcontext)

## get_asgi_version

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L193)

```python
def get_asgi_version(ctx: HTTPContext):
```

Returns `HTTPContext.asgi_version`.

#### See also

- [HTTPContext](#httpcontext)

## get_client

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L213)

```python
def get_client(ctx: HTTPContext):
```

Returns `HTTPContext.client`.

#### See also

- [HTTPContext](#httpcontext)

## get_closed

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L248)

```python
def get_closed(ctx: HTTPContext):
```

Returns `HTTPContext.closed`.

#### See also

- [HTTPContext](#httpcontext)

## get_http_version

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L203)

```python
def get_http_version(ctx: HTTPContext):
```

Returns `HTTPContext.http_version`.

#### See also

- [HTTPContext](#httpcontext)

## get_received

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L238)

```python
def get_received(ctx: HTTPContext):
```

Returns `HTTPContext.received`.

#### See also

- [HTTPContext](#httpcontext)

## get_request_body

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L183)

```python
def get_request_body(ctx: HTTPContext):
```

Returns `HTTPContext.request_body`.

#### See also

- [HTTPContext](#httpcontext)

## get_request_headers

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L178)

```python
def get_request_headers(ctx: HTTPContext):
```

Returns `HTTPContext.request_headers`.

#### See also

- [HTTPContext](#httpcontext)

## get_request_method

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L163)

```python
def get_request_method(ctx: HTTPContext):
```

Returns `HTTPContext.request_method`.

#### See also

- [HTTPContext](#httpcontext)

## get_request_path

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L168)

```python
def get_request_path(ctx: HTTPContext):
```

Returns `HTTPContext.request_path`.

#### See also

- [HTTPContext](#httpcontext)

## get_request_query_string

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L173)

```python
def get_request_query_string(ctx: HTTPContext):
```

Returns `HTTPContext.request_query_string`.

#### See also

- [HTTPContext](#httpcontext)

## get_response_body

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L223)

```python
def get_response_body(ctx: HTTPContext):
```

Returns `HTTPContext.response_body`.

#### See also

- [HTTPContext](#httpcontext)

## get_response_headers

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L228)

```python
def get_response_headers(ctx: HTTPContext):
```

Returns `HTTPContext.response_headers`.

#### See also

- [HTTPContext](#httpcontext)

## get_response_status

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L233)

```python
def get_response_status(ctx: HTTPContext):
```

Returns `HTTPContext.response_status`.

#### See also

- [HTTPContext](#httpcontext)

## get_scheme

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L208)

```python
def get_scheme(ctx: HTTPContext):
```

Returns `HTTPContext.scheme`.

#### See also

- [HTTPContext](#httpcontext)

## get_scope_type

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L188)

```python
def get_scope_type(ctx: HTTPContext):
```

Returns `HTTPContext.scope_type`.

#### See also

- [HTTPContext](#httpcontext)

## get_server

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L218)

```python
def get_server(ctx: HTTPContext):
```

Returns `HTTPContext.server`.

#### See also

- [HTTPContext](#httpcontext)

## get_started

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L243)

```python
def get_started(ctx: HTTPContext):
```

Returns `HTTPContext.started`.

#### See also

- [HTTPContext](#httpcontext)

## send_message

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L82)

```python
@hof1
@future.returns
async def send_message(msg: Message, ctx: HTTPContext) -> HTTPContext:
```

Sends message from [HTTPContext](#httpcontext) to client.

#### Arguments

- `msg` *Message* - to send.
- `ctx` *HTTPContext* - to send from.

#### Returns

- `HTTPContext` - context.

#### See also

- [HTTPContext](#httpcontext)
- [Message](../context.md#message)

## set_closed

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L153)

```python
@hof1
def set_closed(value: bool, ctx: HTTPContext) -> HTTPContext:
```

Sync [HTTPContext](#httpcontext) that sets `closed` to `value`.

#### See also

- [HTTPContext](#httpcontext)

## set_received

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L139)

```python
@hof1
def set_received(value: bool, ctx: HTTPContext) -> HTTPContext:
```

Sync [HTTPContext](#httpcontext) that sets `received` to `value`.

#### See also

- [HTTPContext](#httpcontext)

## set_response_body

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L98)

```python
@hof1
def set_response_body(data: bytes, ctx: HTTPContext) -> HTTPContext:
```

Set response body.

Response body is some byte string so default `HTTPFunc` accepts `bytes`.

#### Arguments

- `data` *bytes* - body to set.
- `ctx` *HTTPContext* - context to set body to.

#### See also

- [HTTPContext](#httpcontext)

## set_response_header

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L124)

```python
@hof2
def set_response_header(
    name: str,
    value: str,
    ctx: HTTPContext,
) -> HTTPContext:
```

Set `value` for response header `name`.

#### Arguments

- `name` *str* - header name.
- `value` *str* - header value.
- `ctx` *HTTPContext* - to set header to.

#### See also

- [HTTPContext](#httpcontext)

## set_response_status

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L112)

```python
@hof1
def set_response_status(code: int, ctx: HTTPContext) -> HTTPContext:
```

Set response status code.

#### Arguments

- `code` *int* - status code to set.
- `ctx` *HTTPContext* - context to set status code to.

#### See also

- [HTTPContext](#httpcontext)

## set_started

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/context.py#L146)

```python
@hof1
def set_started(value: bool, ctx: HTTPContext) -> HTTPContext:
```

Sync [HTTPContext](#httpcontext) that sets `started` to `value`.

#### See also

- [HTTPContext](#httpcontext)
