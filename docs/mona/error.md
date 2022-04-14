# Error

> Auto-generated documentation for [mona.error](https://github.com/katunilya/mona/blob/main/mona/error.py) module.

- [Mona](../README.md#mona-index) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Error
    - [Error](#error)
    - [HttpError](#httperror)

## Error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/error.py#L5)

```python
dataclass
class Error(Exception):
```

Base class for exception.

## HttpError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/error.py#L12)

```python
dataclass
class HttpError(Error):
```

Base class for exception sent over http.

#### See also

- [Error](#error)
