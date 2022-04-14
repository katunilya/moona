# Error

> Auto-generated documentation for [mona.error](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/error.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Error
    - [Error](#error)
    - [HttpError](#httperror)

## Error

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/error.py#L5)

```python
dataclass
class Error(Exception):
```

Base class for exception.

## HttpError

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/error.py#L12)

```python
dataclass
class HttpError(Error):
```

Base class for exception sent over http.

#### See also

- [Error](#error)
