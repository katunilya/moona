# Lifespan

> Auto-generated documentation for [mona.handlers.lifespan](https://github.com/katunilya/mona/blob/main/mona/handlers/lifespan.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Lifespan
    - [lifespan_async](#lifespan_async)

## lifespan_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/lifespan.py#L6)

```python
def lifespan_async(
    on_startup: LifespanHandler,
    on_shutdown: LifespanHandler,
) -> LifespanHandler:
```

Handler for "lifespan" scope type.

`on_startup` is called on server startup receiving "lifespan.startup" event and
`on_shutdown` is called on server shutdown receiving "lifespan.shutdown" event.

#### Arguments

- `on_startup` *LifespanHandler* - to call on server startup.
- `on_shutdown` *LifespanHandler* - to call on server shutdown.

#### See also

- [LifespanHandler](core.md#lifespanhandler)
