# Events

> Auto-generated documentation for [mona.req.events](https://github.com/katunilya/mona/blob/main/mona/req/events.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Events
    - [receive_body](#receive_body)

## receive_body

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/events.py#L4)

```python
@state.accepts_right
async def receive_body(ctx: context.Context) -> context.Context:
```

Read entire request body and place it into context as ByteString.
