# Asgi

> Auto-generated documentation for [mona.asgi](https://github.com/katunilya/mona/blob/main/mona/asgi.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Asgi
    - [create](#create)

## create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/asgi.py#L4)

```python
def create(handler: handler.Handler) -> context.ASGIServer:
```

Constructs ASGI Server function from sequence of handlers.

#### Returns

- `context.ASGIServer` - ASGI function
