# Body

> Auto-generated documentation for [mona.res.body](https://github.com/katunilya/mona/blob/main/mona/res/body.py) module.

- [Mona](../../README.md#mona-index) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Res](index.md#res) / Body
    - [set_body_bytes](#set_body_bytes)
    - [set_body_from_bytes](#set_body_from_bytes)
    - [set_body_from_dict](#set_body_from_dict)
    - [set_body_from_pydantic](#set_body_from_pydantic)
    - [set_body_text](#set_body_text)

## set_body_bytes

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L12)

```python
def set_body_bytes(body: typing.ByteString) -> handler.Handler:
```

Set response body from byte string.

## set_body_from_bytes

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L35)

```python
def set_body_from_bytes(
    function: typing.Callable[
        [
            context.Context,
        ],
        future.Future[state.RE[typing.ByteString]],
    ],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_from_dict

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L66)

```python
def set_body_from_dict(
    function: typing.Callable[[context.Context], future.Future[state.RE[dict]]],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_from_pydantic

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L97)

```python
def set_body_from_pydantic(
    function: typing.Callable[
        [
            context.Context,
        ],
        future.Future[state.RE[pydantic.BaseModel]],
    ],
) -> handler.Handler:
```

Set body from function calculation result.

## set_body_text

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/res/body.py#L23)

```python
def set_body_text(body: str) -> handler.Handler:
```

Set response body from string.
