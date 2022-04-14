# Events

> Auto-generated documentation for [mona.res.events](https://github.com/katunilya/mona/blob/main/mona/res/events.py) module.

- [Mona](../../README.md#mona-index) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Res](index.md#res) / Events
    - [send_body](#send_body)
    - [send_start](#send_start)

## send_body

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/events.py#L20)

```python
@state.accepts_right
async def send_body(ctx: context.Context) -> context.StateContext:
```

Send response body event, which closes connection between server and client.

## send_start

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/events.py#L4)

```python
@state.accepts_right
async def send_start(ctx: context.Context) -> context.StateContext:
```

Send response start event accroding to ASGI specs.
