# Response Body

> Auto-generated documentation for [moona.http.response_body](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Response Body
    - [json](#json)
    - [negotiate](#negotiate)
    - [raw](#raw)
    - [set_json](#set_json)
    - [set_raw](#set_raw)
    - [set_text](#set_text)
    - [text](#text)

## json

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L69)

```python
def json(data: BaseModel) -> HTTPHandler:
```

Respond client with passed `BaseModel` json representation.

Also sets "Content-Type: application/json" response header.

#### Arguments

- `data` *BaseModel* - response body.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## negotiate

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L80)

```python
def negotiate(data: bytes | str | BaseModel) -> HTTPHandler:
```

Respond client with passed data based on its type.

#### Arguments

data (bytes | str | BaseModel): to respond with.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## raw

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L49)

```python
def raw(data: bytes) -> HTTPHandler:
```

Respond client with raw passed `bytes`.

#### Arguments

- `data` *bytes* - response body.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## set_json

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L37)

```python
def set_json(data: BaseModel) -> HTTPHandler:
```

Sets response body to passed object json representation.

Also sets "Content-Type: application/json" response header.

#### Arguments

- `data` *BaseModel* - body.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## set_raw

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L14)

```python
@handler1
def set_raw(
    data: bytes,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Sets response body to passed `bytes`.

#### Arguments

- `data` *bytes* - body.
- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to run on.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)

## set_text

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L26)

```python
def set_text(data: str) -> HTTPHandler:
```

Sets response body to passed `str`.

Also sets "Content-Type: text/plain" response header.

#### Arguments

- `data` *str* - body.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## text

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/response_body.py#L58)

```python
def text(data: str) -> HTTPHandler:
```

Respond client with passed `str`.

Also sets "Content-Type: text/plain" response header.

#### Arguments

- `data` *str* - response body.

#### See also

- [HTTPHandler](handlers.md#httphandler)
