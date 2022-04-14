# Body

> Auto-generated documentation for [mona.req.body](https://github.com/katunilya/mona/blob/main/mona/req/body.py) module.

- [Mona](../../README.md#mona-index) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Body
    - [RequestBodyIsNotReceivedError](#requestbodyisnotreceivederror)
    - [TypeIsNotDataclassError](#typeisnotdataclasserror)
    - [TypeIsNotPydanticBaseModel](#typeisnotpydanticbasemodel)
    - [take_body](#take_body)
    - [take_body_as_dataclass](#take_body_as_dataclass)
    - [take_body_as_dict](#take_body_as_dict)
    - [take_body_as_pydantic](#take_body_as_pydantic)
    - [take_body_as_str](#take_body_as_str)

## RequestBodyIsNotReceivedError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L13)

```python
dataclass
class RequestBodyIsNotReceivedError(Error):
    def __init__():
```

Request body is None and cannot be taken.

#### See also

- [Error](../error.md#error)

## TypeIsNotDataclassError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L24)

```python
dataclass
class TypeIsNotDataclassError(Error):
    def __init__(t: Type):
```

Passed type is not dataclass.

#### See also

- [Error](../error.md#error)

## TypeIsNotPydanticBaseModel

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L38)

```python
dataclass
class TypeIsNotPydanticBaseModel(Error):
    def __init__(t: Type):
```

Passed type is not `pydantic.BaseModel`.

#### See also

- [Error](../error.md#error)

## take_body

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L51)

```python
def take_body(ctx: Context) -> RE[ByteString]:
```

Take request body as byte string.

#### See also

- [Context](../context.md#context)

## take_body_as_dataclass

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L67)

```python
def take_body_as_dataclass(dataclass_type: Type) -> Callable[[Context], RE]:
```

Take request body as dataclass.

#### See also

- [Context](../context.md#context)
- [RE](../state.md#re)

## take_body_as_dict

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L59)

```python
def take_body_as_dict(ctx: Context) -> RE[dict]:
```

Take request body as dict.

#### See also

- [Context](../context.md#context)

## take_body_as_pydantic

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L81)

```python
def take_body_as_pydantic(
    model_type: Type[BaseModel],
) -> Callable[[Context], RE[BaseModel]]:
```

Take request body as pydantic BaseModel.

#### See also

- [Context](../context.md#context)

## take_body_as_str

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/body.py#L97)

```python
def take_body_as_str(ctx: Context) -> RE[str]:
```

Take request body as str.

#### See also

- [Context](../context.md#context)
