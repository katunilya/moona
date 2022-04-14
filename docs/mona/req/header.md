# Header

> Auto-generated documentation for [mona.req.header](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/req/header.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Header
    - [has_header](#has_header)
    - [take_headers](#take_headers)

## has_header

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/req/header.py#L6)

```python
def has_header(
    key: str,
    value: str,
    required: bool = False,
) -> handler.Handler:
```

Continue execution if request has header `key` of `value`.

Accpts only context in RIGHT state. Returns context in RIGHT state if header with
required value is present in request headers. Returns context in WRONG state if not.

#### Arguments

- `key` *str* - of header
- `value` *str* - of header

#### Returns

- `handler3.Handler` - handler

## take_headers

[[find in source code]](https://github.com/katunilya/mona/blob/2-provide-multiple-examples-of-using-library/mona/req/header.py#L32)

```python
def take_headers(ctx: context.Context) -> state.State[dict[str, str]]:
```

Extracts request header as dict of strings.

#### Arguments

- `ctx` *context.Context* - source

#### Returns

- `state.State[dict[str,` *str]]* - headers
