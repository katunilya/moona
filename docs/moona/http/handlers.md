# Handlers

> Auto-generated documentation for [moona.http.handlers](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py) module.

- [Moona](../../README.md#moona-index) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Handlers
    - [HTTPHandler](#httphandler)
        - [HTTPHandler().compose](#httphandlercompose)
    - [choose](#choose)
    - [compose](#compose)
    - [end](#end)
    - [handle_func](#handle_func)
    - [handle_func_sync](#handle_func_sync)
    - [handler](#handler)
    - [handler1](#handler1)
    - [handler2](#handler2)
    - [handler3](#handler3)
    - [skip](#skip)

## HTTPHandler

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L41)

```python
dataclass(frozen=True, slots=True)
class HTTPHandler():
    def __init__(handler: _HTTPHandler) -> None:
```

Abstraction over function that hander `HTTPContext`.

### HTTPHandler().compose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L54)

```python
def compose(h: _HTTPHandler) -> HTTPHandler:
```

Compose 2 [HTTPHandler](#httphandler)s into one.

#### Arguments

- `h2` *_HTTPHandler* - to run next.

#### Returns

- `HTTPHandler` - resulting handler.

## choose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L141)

```python
def choose(handlers: list[HTTPHandler]) -> HTTPHandler:
```

Iterate though handlers till one would return some `HTTPContext`.

#### Arguments

- `handlers` *list[HTTPHandler]* - to iterate through.

#### Returns

- `HTTPHandler` - result.

#### See also

- [HTTPHandler](#httphandler)

## compose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L15)

```python
def compose(h1: _HTTPHandler, h2: _HTTPHandler) -> HTTPHandler:
```

Compose 2 [HTTPHandler](#httphandler)s into one.

#### Arguments

- `h1` *_HTTPHandler* - to run first.
- `h2` *_HTTPHandler* - to run second.

#### Returns

- `HTTPHandler` - resulting handler.

#### See also

- [HTTPHandler](#httphandler)

## end

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L223)

```python
def end(ctx: HTTPContext) -> Future[HTTPContext]:
```

[HTTPFunc](#handlers) that finishes the pipeline of request handling.

#### Arguments

- `ctx` *HTTPContext* - to end.

#### Returns

- `Future[HTTPContext]` - ended ctx.

#### See also

- [HTTPContext](context.md#httpcontext)

## handle_func

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L79)

```python
def handle_func(func: HTTPFunc) -> HTTPHandler:
```

Converts [HTTPFunc](#handlers) to [HTTPHandler](#httphandler).

#### Arguments

- `func` *HTTPFunc* - to convert to [HTTPHandler](#httphandler).

#### Returns

- `HTTPHandler` - result.

#### See also

- [HTTPFunc](#httpfunc)
- [HTTPHandler](#httphandler)

## handle_func_sync

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L104)

```python
def handle_func_sync(
    func: Callable[[HTTPContext], HTTPContext | None],
) -> HTTPHandler:
```

Converts sync [HTTPFunc](#handlers) to [HTTPHandler](#httphandler).

#### Arguments

func (Callable[[HTTPContext], HTTPContext | None]): to convert to [HTTPHandler](#httphandler).

#### Returns

- `HTTPHandler` - result.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPHandler](#httphandler)

## handler

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L74)

```python
def handler(func: _HTTPHandler) -> HTTPHandler:
```

Decorator that converts function to HTTPHandler callable.

#### See also

- [HTTPHandler](#httphandler)

## handler1

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L169)

```python
def handler1(
    func: Callable[[A, HTTPFunc, HTTPContext], Future[HTTPContext | None]],
) -> Callable[[A], HTTPHandler]:
```

Decorator for HTTPHandlers with 1 additional argument.

Makes it "curried".

#### See also

- [A](#a)
- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](#httpfunc)
- [HTTPHandler](#httphandler)

## handler2

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L183)

```python
def handler2(
    func: Callable[[A, B, HTTPFunc, HTTPContext], Future[HTTPContext | None]],
) -> Callable[[A, B], HTTPHandler]:
```

Decorator for HTTPHandlers with 2 additional arguments.

Makes it "curried".

#### See also

- [A](#a)
- [B](#b)
- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](#httpfunc)
- [HTTPHandler](#httphandler)

## handler3

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L197)

```python
def handler3(
    func: Callable[[A, B, C, HTTPFunc, HTTPContext], Future[HTTPContext | None]],
) -> Callable[[A, B, C], HTTPHandler]:
```

Decorator for HTTPHandlers with 1 additional argument.

Makes it "curried".

#### See also

- [A](#a)
- [B](#b)
- [C](#c)
- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](#httpfunc)
- [HTTPHandler](#httphandler)

## skip

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/handlers.py#L211)

```python
def skip(_: HTTPContext) -> Future[None]:
```

[HTTPFunc](#handlers) that skips pipeline by returning `None` instead of context.

#### Arguments

- `_` *HTTPContext* - ctx we don't care of.

#### Returns

- `Future[None]` - result.

#### See also

- [HTTPContext](context.md#httpcontext)
