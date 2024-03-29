# Handlers

> Auto-generated documentation for [moona.lifespan.handlers](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Lifespan](index.md#lifespan) / Handlers
    - [LifespanHandler](#lifespanhandler)
        - [LifespanHandler().compose](#lifespanhandlercompose)
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

## LifespanHandler

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L40)

```python
dataclass(frozen=True, slots=True)
class LifespanHandler():
    def __init__(handler: _LifespanHandler) -> None:
```

Abstraction over function that hander `LifespanContext`.

### LifespanHandler().compose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L53)

```python
def compose(h: _LifespanHandler) -> LifespanHandler:
```

Compose 2 [LifespanHandler](#lifespanhandler)s into one.

#### Arguments

- `h2` *_LifespanHandler* - to run next.

#### Returns

- `LifespanHandler` - resulting handler.

## choose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L140)

```python
def choose(handlers: list[LifespanHandler]) -> LifespanHandler:
```

Iterate though handlers till one would return some `LifespanContext`.

#### Arguments

- `handlers` *list[LifespanHandler]* - to iterate through.

#### Returns

- `LifespanHandler` - result.

#### See also

- [LifespanHandler](#lifespanhandler)

## compose

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L17)

```python
def compose(h1: _LifespanHandler, h2: _LifespanHandler) -> LifespanHandler:
```

Compose 2 [LifespanHandler](#lifespanhandler)s into one.

#### Arguments

- `h1` *_LifespanHandler* - to run first.
- `h2` *_LifespanHandler* - to run second.

#### Returns

- `LifespanHandler` - resulting handler.

#### See also

- [LifespanHandler](#lifespanhandler)

## end

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L228)

```python
def end(ctx: LifespanContext) -> future[LifespanContext]:
```

[LifespanFunc](#handlers) that finishes the pipeline of request handling.

#### Arguments

- `ctx` *LifespanContext* - to end.

#### Returns

- `future[LifespanContext]` - ended ctx.

## handle_func

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L78)

```python
def handle_func(func: LifespanFunc) -> LifespanHandler:
```

Converts [LifespanFunc](#handlers) to [LifespanHandler](#lifespanhandler).

#### Arguments

- `func` *LifespanFunc* - to convert to [LifespanHandler](#lifespanhandler).

#### Returns

- `LifespanHandler` - result.

#### See also

- [LifespanFunc](#lifespanfunc)
- [LifespanHandler](#lifespanhandler)

## handle_func_sync

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L101)

```python
def handle_func_sync(
    func: Callable[[LifespanContext], LifespanContext | None],
) -> LifespanHandler:
```

Converts sync [LifespanFunc](#handlers) to [LifespanHandler](#lifespanhandler).

#### Arguments

func (Callable[[LifespanContext], LifespanContext | None]): to convert to
[LifespanHandler](#lifespanhandler).

#### Returns

- `LifespanHandler` - result.

#### See also

- [LifespanHandler](#lifespanhandler)

## handler

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L73)

```python
def handler(func: _LifespanHandler) -> LifespanHandler:
```

Decorator that converts function to LifespanHandler callable.

#### See also

- [LifespanHandler](#lifespanhandler)

## handler1

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L170)

```python
def handler1(
    func: Callable[
        [
            A,
            LifespanFunc,
            LifespanContext,
        ],
        future[LifespanContext | None],
    ],
) -> Callable[[A], LifespanHandler]:
```

Decorator for LifespanHandlers with 1 additional argument.

Makes it "curried".

#### See also

- [A](#a)
- [LifespanFunc](#lifespanfunc)
- [LifespanHandler](#lifespanhandler)

## handler2

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L184)

```python
def handler2(
    func: Callable[
        [
            A,
            B,
            LifespanFunc,
            LifespanContext,
        ],
        future[LifespanContext | None],
    ],
) -> Callable[[A, B], LifespanHandler]:
```

Decorator for LifespanHandlers with 2 additional arguments.

Makes it "curried".

#### See also

- [A](#a)
- [B](#b)
- [LifespanFunc](#lifespanfunc)
- [LifespanHandler](#lifespanhandler)

## handler3

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L200)

```python
def handler3(
    func: Callable[
        [
            A,
            B,
            C,
            LifespanFunc,
            LifespanContext,
        ],
        future[LifespanContext | None],
    ],
) -> Callable[[A, B, C], LifespanHandler]:
```

Decorator for LifespanHandlers with 1 additional argument.

Makes it "curried".

#### See also

- [A](#a)
- [B](#b)
- [C](#c)
- [LifespanFunc](#lifespanfunc)
- [LifespanHandler](#lifespanhandler)

## skip

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/handlers.py#L216)

```python
def skip(_: LifespanContext) -> future[None]:
```

[LifespanFunc](#handlers) that skips pipeline by returning `None` instead of context.

#### Arguments

- `_` *LifespanContext* - ctx we don't care of.

#### Returns

- `future[None]` - result.
