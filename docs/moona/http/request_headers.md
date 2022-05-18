# Request Headers

> Auto-generated documentation for [moona.http.request_headers](https://github.com/katunilya/moona/blob/main/moona/http/request_headers.py) module.

- [Moona](../../README.md#moona-index) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Request Headers
    - [has_header](#has_header)
    - [matches_header](#matches_header)

## has_header

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_headers.py#L9)

```python
def has_header(name: str) -> HTTPHandler:
```

Processes next `HTTPFunc` only when request has passed header.

#### Arguments

- `name` *str* - to check for.

## matches_header

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_headers.py#L28)

```python
def matches_header(name: str, value: str) -> HTTPHandler:
```

Processes next `HTTPFunc` only when request has valid headers.

#### Arguments

- `name` *str* - to check header.
- `value` *str* - to check. Optional. If not passed, than presence of header is
checked.
