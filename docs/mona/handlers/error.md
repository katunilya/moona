# Error

> Auto-generated documentation for [mona.handlers.error](https://github.com/katunilya/mona/blob/main/mona/handlers/error.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Error
    - [send_error_async](#send_error_async)

## send_error_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/error.py#L8)

```python
@error_handler
def send_error_async(err: ContextError) -> HTTPContext:
```

Default handler for all `HTTPContextErrors`.

Sets response status to `err.status`, response body to `err.message`.

Also sets headers:
* Content-Length: XXX
* Content-Type: text/plain

#### See also

- [ContextError](../core.md#contexterror)
- [HTTPContext](../core.md#httpcontext)
- [error_handler](core.md#error_handler)
