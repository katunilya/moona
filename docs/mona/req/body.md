# Body

> Auto-generated documentation for [mona.req.body](https://github.com/katunilya/mona/blob/main/mona/req/body.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Body
    - [RequestBodyIsNotReceivedError](#requestbodyisnotreceivederror)
    - [TypeIsNotDataclassError](#typeisnotdataclasserror)
    - [TypeIsNotPydanticBaseModelError](#typeisnotpydanticbasemodelerror)
    - [take_body](#take_body)
    - [take_body_as_dataclass](#take_body_as_dataclass)
    - [take_body_as_dict](#take_body_as_dict)
    - [take_body_as_pydantic](#take_body_as_pydantic)
    - [take_body_as_str](#take_body_as_str)

## RequestBodyIsNotReceivedError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L11)

```python
dataclasses.dataclass
class RequestBodyIsNotReceivedError(Exception):
    def __init__():
```

Request body is None and cannot be taken.

## TypeIsNotDataclassError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L22)

```python
dataclasses.dataclass
class TypeIsNotDataclassError(Exception):
    def __init__(t: typing.Type):
```

Passed type is not dataclass.

## TypeIsNotPydanticBaseModelError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L36)

```python
dataclasses.dataclass
class TypeIsNotPydanticBaseModelError(Exception):
    def __init__(t: typing.Type):
```

Passed type is not `pydantic.BaseModel`.

## take_body

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L49)

```python
def take_body(ctx: context.Context) -> state.ESafe[bytes]:
```

Take request body as byte string.

## take_body_as_dataclass

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L65)

```python
def take_body_as_dataclass(
    dataclass_type: typing.Type,
) -> typing.Callable[[context.Context], state.ESafe[object]]:
```

Take request body as dataclass.

## take_body_as_dict

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L57)

```python
def take_body_as_dict(ctx: context.Context) -> state.ESafe[dict]:
```

Take request body as dict.

## take_body_as_pydantic

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L83)

```python
def take_body_as_pydantic(
    model_type: typing.Type[pydantic.BaseModel],
) -> typing.Callable[[context.Context], state.ESafe[pydantic.BaseModel]]:
```

Take request body as pydantic BaseModel.

## take_body_as_str

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L101)

```python
def take_body_as_str(ctx: context.Context) -> state.ESafe[str]:
```

Take request body as str.
