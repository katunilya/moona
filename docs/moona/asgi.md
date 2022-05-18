# Asgi

> Auto-generated documentation for [moona.asgi](https://github.com/katunilya/moona/blob/main/moona/asgi.py) module.

- [Moona](../README.md#-moona) / [Modules](../MODULES.md#moona-modules) / [Moona](index.md#moona) / Asgi
    - [create](#create)

## create

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/asgi.py#L47)

```python
def create(
    http_handler: http.HTTPHandler = _default_http_handler,
    startup_handler: lifespan.LifespanHandler = None,
    shutdown_handler: lifespan.LifespanHandler = None,
) -> ASGIApp:
```

Constructs ASGI Server function from passed handler.

Supports 2 types of request scopes: "http" and "lifetime". For "http" scope
`HTTPContext` is created and used as an argument for the `handler` (via `Future`).
For "lifetime" `LifetimeContext` is created and also used as argument for `handler`.

#### Notes

* https://asgi.readthedocs.io/en/latest/specs/main.html#applications

#### Arguments

- `http_handler` *HTTPHandler* - optional argument for handling "http" requests.
- `on_startup_handler` *LifespanHandler* - optional for handlers to be executed on
server startup
- `on_shutdown_handler` *LifespanHandler* - optional for handlers to be executed on
server shutdown

#### Returns

- `ASGIApp` - ASGI function based on ASGI Specification.

#### See also

- [ASGIApp](context.md#asgiapp)
