# Context

> Auto-generated documentation for [moona.lifespan.context](https://github.com/katunilya/moona/blob/main/moona/lifespan/context.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Lifespan](index.md#lifespan) / Context
    - [LifespanContext](#lifespancontext)

## LifespanContext

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/lifespan/context.py#L9)

```python
dataclass(slots=True)
class LifespanContext(BaseContext):
    def __init__(scope: Scope, receive: Receive, send: Send) -> None:
```

Context for handling actions performed on startup and shutdown.

It contains all the information required based on ASGI Lifespan Specification.

#### Notes

https://asgi.readthedocs.io/en/latest/specs/lifespan.html

#### Attributes

- `type_` *str* - type of context. Must be "lifespan".
- `asgi_version` *str* - version of the ASGI spec.
- `asgi_spec_version` *str* - The version of this spec being used. Optional; if
missing defaults to "1.0".

#### See also

- [BaseContext](../context.md#basecontext)
- [Receive](../context.md#receive)
- [Scope](../context.md#scope)
- [Send](../context.md#send)
