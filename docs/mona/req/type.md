# Type

> Auto-generated documentation for [mona.req.type](https://github.com/katunilya/mona/blob/main/mona/req/type.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Type
    - [on_http](#on_http)

## on_http

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/type.py#L4)

```python
@state.accepts_right
def on_http(ctx: context.Context) -> context.StateContext:
```

Returns right `Context` when request type is "http".
