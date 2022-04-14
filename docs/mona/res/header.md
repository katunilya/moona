# Header

> Auto-generated documentation for [mona.res.header](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/res/header.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Res](index.md#res) / Header
    - [set_header](#set_header)
    - [set_header_content_type](#set_header_content_type)

## set_header

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/res/header.py#L4)

```python
def set_header(key: str, value: str) -> handler.Handler:
```

Generates handler that sets passed key value pair into response headers.

## set_header_content_type

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/res/header.py#L17)

```python
def set_header_content_type(value: str) -> handler.Handler:
```

Sets value for `Content-Type` header of response.
