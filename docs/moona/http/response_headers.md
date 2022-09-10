# Response Headers

> Auto-generated documentation for [moona.http.response_headers](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Response Headers
    - [auto_content_length](#auto_content_length)
    - [content_length](#content_length)
    - [content_type](#content_type)
    - [content_type_application_json](#content_type_application_json)
    - [content_type_text_plain](#content_type_text_plain)
    - [header](#header)

## auto_content_length

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L79)

```python
@handle_func_sync
def auto_content_length(ctx: HTTPContext) -> HTTPContext:
```

Sets "Content-Length" to current response body.

If body is `None` than 0 length is set.

#### Arguments

- `ctx` *HTTPContext* - to set header to.

#### See also

- [HTTPContext](context.md#httpcontext)
- [handle_func_sync](handlers.md#handle_func_sync)

## content_length

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L70)

```python
def content_length(value: int) -> HTTPHandler:
```

`HTTPHandler` that sets "Content-Length` response header.

#### Arguments

- `value` *int* - of header

#### See also

- [HTTPHandler](handlers.md#httphandler)

## content_type

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L28)

```python
def content_type(value: str):
```

`HTTPHandler` that sets "Content-Type" response header.

#### Arguments

- `value` *str* - of header.

#### Returns

- `HTTPHandler` - handler.

## content_type_application_json

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L40)

```python
def content_type_application_json(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Sets "Content-Type: application/json" response header.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### Returns

future[HTTPContext | None]: result

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)

## content_type_text_plain

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L55)

```python
def content_type_text_plain(
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Sets "Content-Type: text/plain" response header.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process

#### Returns

future[HTTPContext | None]: result.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)

## header

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_headers.py#L7)

```python
@handler2
def header(
    name: str,
    value: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

`HTTPHandler` that sets response header.

#### Arguments

- `name` *str* - of header.
- `value` *str* - of header.
- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### Returns

future[HTTPContext | None]: result.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler2](handlers.md#handler2)
