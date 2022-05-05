# Method

> Auto-generated documentation for [mona.handlers.method](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Method
    - [WrongHTTPMethodError](#wronghttpmethoderror)
    - [CONNECT](#connect)
    - [DELETE](#delete)
    - [GET](#get)
    - [HEAD](#head)
    - [OPTIONS](#options)
    - [PATCH](#patch)
    - [POST](#post)
    - [PUT](#put)
    - [TRACE](#trace)
    - [method](#method)

## WrongHTTPMethodError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L7)

```python
class WrongHTTPMethodError(ContextError):
    def __init__(ctx: HTTPContext, method: str) -> None:
```

`HTTPContext` is handled via wrong handler based on method mismatch.

#### See also

- [ContextError](../core.md#contexterror)
- [HTTPContext](../core.md#httpcontext)

## CONNECT

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L91)

```python
@http_handler
def CONNECT(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on CONNECT method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## DELETE

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L67)

```python
@http_handler
def DELETE(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on DELETE method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## GET

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L43)

```python
@http_handler
def GET(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on GET method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## HEAD

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L79)

```python
@http_handler
def HEAD(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on HEAD method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## OPTIONS

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L73)

```python
@http_handler
def OPTIONS(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on OPTIONS method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## PATCH

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L55)

```python
@http_handler
def PATCH(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on PATCH method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## POST

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L49)

```python
@http_handler
def POST(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on POST method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## PUT

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L61)

```python
@http_handler
def PUT(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on PUT method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## TRACE

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L85)

```python
@http_handler
def TRACE(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that proceeds `HTTPContext` only on TRACE method.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## method

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/method.py#L18)

```python
def method(method_: str) -> HTTPHandler:
```

Continues execution if request method is passed method.

#### See also

- [HTTPHandler](core.md#httphandler)
