# Body

> Auto-generated documentation for [mona.res.body](https://github.com/katunilya/mona/blob/main/mona/res/body.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Res](index.md#res) / Body
    - [set_body_bytes](#set_body_bytes)
    - [set_body_from_bytes](#set_body_from_bytes)
    - [set_body_from_dict](#set_body_from_dict)
    - [set_body_from_pydantic](#set_body_from_pydantic)
    - [set_body_from_text](#set_body_from_text)
    - [set_body_text](#set_body_text)

## set_body_bytes

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L11)

```python
def set_body_bytes(body: bytes) -> handler.Handler:
```

Set response body from byte string.

## set_body_from_bytes

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L34)

```python
def set_body_from_bytes(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[bytes]]],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_from_dict

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L98)

```python
def set_body_from_dict(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[dict]]],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_from_pydantic

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L130)

```python
def set_body_from_pydantic(
    function: typing.Callable[
        [
            context.Context,
        ],
        future.Future[state.ESafe[pydantic.BaseModel]],
    ],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_from_text

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L64)

```python
def set_body_from_text(
    function: typing.Callable[[context.Context], future.Future[state.ESafe[str]]],
) -> handler.Handler:
```

Set body from function calculation result (str).

## set_body_text

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L22)

```python
def set_body_text(body: str) -> handler.Handler:
```

Set response body from string.
