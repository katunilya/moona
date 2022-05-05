# Header

> Auto-generated documentation for [mona.handlers.header](https://github.com/katunilya/mona/blob/main/mona/handlers/header.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Header
    - [get_header](#get_header)
    - [get_headers](#get_headers)
    - [remove_header](#remove_header)
    - [set_header](#set_header)

## get_header

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/header.py#L74)

```python
def get_header(name: str) -> Callable[[HTTPContext], Maybe[tuple[str, str]]]:
```

Try to get concrete `HTTPRequest` header by name.

If `name` is present in dictionary of headers than `Some` header is returned.
Otherwise `Nothing`.

#### Arguments

- `name` *str* - name of the header to try to get.

#### Returns

Callable[[HTTPContext], Maybe[tuple[str, str]]]: function that actually returns
headers.

#### See also

- [HTTPContext](../core.md#httpcontext)

## get_headers

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/header.py#L101)

```python
def get_headers(ctx: HTTPContext) -> Maybe[dict[str, str]]:
```

Try to get all `HTTPRequest` headers.

If `HTTPRequest` headers are empty dictionary than `Nothing` is returned. Otherwise
`Some` headers.

#### Arguments

- `ctx` *HTTPContext* - to get headers from.

#### Returns

- `Maybe[dict[str,` *str]]* - `None`-safe `HTTPRequest` headers.

#### See also

- [HTTPContext](../core.md#httpcontext)

## remove_header

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/header.py#L42)

```python
def remove_header(name: str) -> HTTPHandler:
```

`HTTPHandler` that removes response header based on passed header name.

Header name can be passed in any case as based on RFC 2616 headers are
case-insensitive. Due to this and based on ASGI specification response headers are
stored as `dict[bytes, bytes]` where key is lowercase byte string. Passed `name` is
converted to lowercase, than to `bytes` and than key is removed from response
headers `dict`.

Specifications
* RFC 2616 - 4.2 Message Headers -
    https://datatracker.ietf.org/doc/html/rfc2616#section-4.2
* ASGI Specification - Response start event -
    https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event

#### Arguments

- `name` *str* - header name to remove.

#### Returns

- `HTTPHandler` - actually performs remove of response header.

#### See also

- [HTTPHandler](core.md#httphandler)

## set_header

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/header.py#L11)

```python
def set_header(name: str, value: str) -> HTTPHandler:
```

`HTTPHandler` that sets new response header based on passed values.

Response header name is lowercased despite headers are case-insensitive based on
RFC 2616. Also header name and value are converted to `bytes` as `Context` stores
response headers as `dict[bytes, bytes]` based on ASGI specification.

Specifications
* RFC 2616 - 4.2 Message Headers -
    https://datatracker.ietf.org/doc/html/rfc2616#section-4.2
* ASGI Specification - Response start event -
    https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event

#### Arguments

- `name` *str* - header name.
- `value` *str* - header value.

#### Returns

- `HTTPHandler` - actually performs settings response header.

#### See also

- [HTTPHandler](core.md#httphandler)
