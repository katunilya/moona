# Asgi

> Auto-generated documentation for [mona.asgi](https://github.com/katunilya/mona/blob/main/mona/asgi.py) module.

- [Mona](../README.md#mona-index) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Asgi
    - [create](#create)

## create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/asgi.py#L6)

```python
def create(*handlers: handler.Handler) -> context.ASGIServer:
```

Constructs ASGI Server function from sequence of handlers.

#### Returns

- `context.ASGIServer` - ASGI function
