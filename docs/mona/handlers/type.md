# Type

> Auto-generated documentation for [mona.handlers.type](https://github.com/katunilya/mona/blob/main/mona/handlers/type.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Type
    - [WrongContextType](#wrongcontexttype)
    - [http](#http)

## WrongContextType

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/type.py#L5)

```python
class WrongContextType(ContextError):
    def __init__(ctx: BaseContext, type_: str) -> None:
```

`Handler` received Context of wrong type.

#### See also

- [BaseContext](../core.md#basecontext)
- [ContextError](../core.md#contexterror)

## http

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/type.py#L16)

```python
@http_handler
def http(ctx: BaseContext) -> HTTPContextResult:
```

Handler that processes only `HTTPContext`.

#### See also

- [BaseContext](../core.md#basecontext)
- [HTTPContextResult](core.md#httpcontextresult)
- [http_handler](core.md#http_handler)
