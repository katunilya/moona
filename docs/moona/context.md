# Context

> Auto-generated documentation for [moona.context](https://github.com/katunilya/moona/blob/main/moona/context.py) module.

- [Moona](../README.md#moona-index) / [Modules](../MODULES.md#moona-modules) / [Moona](index.md#moona) / Context
    - [BaseContext](#basecontext)

## BaseContext

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/context.py#L14)

```python
class BaseContext(ABC):
```

Base class for each kind of Context handled by application.

Mainly there are 3 kinds:
* `HTTPContext` for "http" request scopes
* `LifespanContext` for "lifetime" request scopes
* `WebsocketContext` (not implemented)
