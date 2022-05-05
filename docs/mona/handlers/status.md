# Status

> Auto-generated documentation for [mona.handlers.status](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Status
    - [set_status](#set_status)
    - [set_status_bad_gateway](#set_status_bad_gateway)
    - [set_status_bad_request](#set_status_bad_request)
    - [set_status_created](#set_status_created)
    - [set_status_forbidden](#set_status_forbidden)
    - [set_status_internal_server_error](#set_status_internal_server_error)
    - [set_status_method_not_allowed](#set_status_method_not_allowed)
    - [set_status_not_found](#set_status_not_found)
    - [set_status_not_implemented](#set_status_not_implemented)
    - [set_status_ok](#set_status_ok)
    - [set_status_unauthorized](#set_status_unauthorized)

## set_status

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L59)

```python
def set_status(code: int) -> HTTPHandler:
```

`HTTPHandler` that sets status code to response.

#### See also

- [HTTPHandler](core.md#httphandler)

## set_status_bad_gateway

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L136)

```python
@http_handler
def set_status_bad_gateway(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to BAD_GATEWAY.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_bad_request

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L94)

```python
@http_handler
def set_status_bad_request(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to BAD_REQUEST.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_created

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L88)

```python
@http_handler
def set_status_created(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to CREATED.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_forbidden

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L106)

```python
@http_handler
def set_status_forbidden(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to FORBIDDEN.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_internal_server_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L124)

```python
@http_handler
def set_status_internal_server_error(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to INTERNAL_SERVER_ERROR.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_method_not_allowed

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L118)

```python
@http_handler
def set_status_method_not_allowed(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to METHOD_NOT_ALLOWED.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_not_found

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L112)

```python
@http_handler
def set_status_not_found(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to NOT_FOUND.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_not_implemented

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L130)

```python
@http_handler
def set_status_not_implemented(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to NOT_IMPLEMENTED.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_ok

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L82)

```python
@http_handler
def set_status_ok(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to OK.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## set_status_unauthorized

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/status.py#L100)

```python
@http_handler
def set_status_unauthorized(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sets `HTTPResponse` status to UNAUTHORIZED.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)
