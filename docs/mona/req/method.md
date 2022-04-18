# Method

> Auto-generated documentation for [mona.req.method](https://github.com/katunilya/mona/blob/main/mona/req/method.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Method
    - [on_connect](#on_connect)
    - [on_delete](#on_delete)
    - [on_get](#on_get)
    - [on_head](#on_head)
    - [on_method](#on_method)
    - [on_options](#on_options)
    - [on_patch](#on_patch)
    - [on_post](#on_post)
    - [on_put](#on_put)
    - [on_trace](#on_trace)

## on_connect

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L72)

```python
@state.accepts_right
def on_connect(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [CONNECT](#method).

## on_delete

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L48)

```python
@state.accepts_right
def on_delete(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [DELETE](#method).

## on_get

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L24)

```python
@state.accepts_right
def on_get(ctx: context.Context) -> context.StateContext:
```

Continue execution if request  method is [GET](#method).

## on_head

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L60)

```python
@state.accepts_right
def on_head(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [HEAD](#method).

## on_method

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L14)

```python
def on_method(method: str) -> handler.Handler:
```

Continue execution if request  method is passed method.

## on_options

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L54)

```python
@state.accepts_right
def on_options(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [OPTIONS](#method).

## on_patch

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L36)

```python
@state.accepts_right
def on_patch(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [PATCH](#method).

## on_post

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L30)

```python
@state.accepts_right
def on_post(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [POST](#method).

## on_put

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L42)

```python
@state.accepts_right
def on_put(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [PUT](#method).

## on_trace

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/method.py#L66)

```python
@state.accepts_right
def on_trace(ctx: context.Context) -> context.StateContext:
```

Continue execution if request method is [TRACE](#method).
