# Asgi

> Auto-generated documentation for [mona.asgi](https://github.com/katunilya/mona/blob/main/mona/asgi.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Asgi
    - [create](#create)

## create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/asgi.py#L16)

```python
def create(handler: Handler) -> ASGIApp:
```

Constructs ASGI Server function from passed handler.

Supports 2 types of request scopes: "http" and "lifetime". For "http" scope
`HTTPContext` is created and used as an argument for the `handler` (via `Future`).
For "lifetime" `LifetimeContext` is created and also used as argument for `handler`.

#### Notes

* https://asgi.readthedocs.io/en/latest/specs/main.html#applications

#### Arguments

- `handler` *Handler* - function that executes on request and processes it.

#### Returns

- `ASGIApp` - ASGI function based on ASGI Specification.

#### See also

- [ASGIApp](core.md#asgiapp)
- [Handler](handlers/core.md#handler)
