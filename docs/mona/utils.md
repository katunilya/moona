# Utils

> Auto-generated documentation for [mona.utils](https://github.com/katunilya/mona/blob/main/mona/utils.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Utils
    - [decode_header](#decode_header)
    - [decode_headers](#decode_headers)
    - [decode_utf_8](#decode_utf_8)
    - [deserialize](#deserialize)
    - [encode_utf_8](#encode_utf_8)
    - [serialize](#serialize)

## decode_header

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L7)

```python
def decode_header(header: tuple[bytes, bytes]) -> tuple[str, str]:
```

## decode_headers

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L12)

```python
def decode_headers(
    headers: Iterable[Iterable[bytes]],
) -> dict[tuple[str, str]]:
```

## decode_utf_8

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L20)

```python
def decode_utf_8(data: bytes) -> str:
```

## deserialize

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L36)

```python
def deserialize(model: Type[BaseModel]) -> Callable[[bytes], BaseModel]:
```

## encode_utf_8

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L24)

```python
def encode_utf_8(data: str) -> bytes:
```

## serialize

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/utils.py#L28)

```python
def serialize(data: BaseModel) -> bytes:
```
