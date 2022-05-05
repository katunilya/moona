# Core

> Auto-generated documentation for [mona.handlers.core](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Core
    - [choose](#choose)
    - [compose](#compose)
    - [do](#do)
    - [error_handler](#error_handler)
    - [http_handler](#http_handler)
    - [lifespan_handler](#lifespan_handler)

## choose

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L80)

```python
def choose(*handlers: Handler) -> Handler:
```

Combinator for choosing the first handler that returns `BaseContext`.

Iterates through multiple passed `handlers` and returns first that returns
`BaseContext`. If all handler return `ContextError` than returns initial
`BaseContext`. If handlers are empty than return initial `BaseContext`.

#### Examples

```python
handler = choose(
    # returns result if method is "GET" and path is "/user"
    get_dataclass('/user', User), # returns result if method is "GET" and path
    is "/users" get_dataclass('/users', Users),
)
```

#### Notes

Handler `get_dataclass` from example are not real.

#### Returns

- `Handler` - resulting [Handler](#core).

#### See also

- [Handler](#handler)

## compose

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L59)

```python
def compose(*handlers: Handler) -> Handler:
```

Combinator for [Handler](#core)s for sequential execution.

Passed [Handler](#core)s are executed one-by-one in passed oreder. Suitable for both sync
and async handlers.

#### Examples

```python
handler: Handler = compose(
    set_status(200_OK),
    set_header("Content-Type", "application/json"),
)

Future.create(Success(ctx)) >> handler
```

#### Returns

- `HTTPHandler` - resulting [HTTPHandler](#core).

#### See also

- [Handler](#handler)

## do

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L119)

```python
def do(ctx: ContextResult, *handlers: Handler) -> Future[ContextResult]:
```

Execute multiple handlers on passed `BaseContext` or `ContextError`.

Actually alias for `Future.do`.

#### Notes

This is possible syntax for executing multiple functions, but `>>` is more
supported.

#### Arguments

- `ctx` *ContextResult* - to use as argument.

#### Returns

- `Future[ContextResult]` - result.

#### See also

- [ContextResult](#contextresult)
- [Handler](#handler)

## error_handler

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L11)

```python
def error_handler(handler: Handler) -> Handler:
```

Decorator for `ContextError` handlers.

This decorator will run handler only when `ContextError` is passed.

#### See also

- [Handler](#handler)

## http_handler

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L36)

```python
def http_handler(handler: HTTPHandler) -> HTTPHandler:
```

Decorator for `HTTPContext` handlers.

This decorator will run this handler only when `HTTPContext` is passed.

#### See also

- [HTTPHandler](#httphandler)

## lifespan_handler

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/core.py#L143)

```python
def lifespan_handler(handler: LifespanHandler) -> LifespanHandler:
```

Decorator for `LifespanContext` handlers on startup and shutdown.

This decorator will proceed only unfinished `LifespanContext`.

#### See also

- [LifespanHandler](#lifespanhandler)
