# Body

> Auto-generated documentation for [mona.handlers.body](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Body
    - [bind_body_bytes_async](#bind_body_bytes_async)
    - [bind_body_json_async](#bind_body_json_async)
    - [bind_body_text_async](#bind_body_text_async)
    - [get_body_bytes_async](#get_body_bytes_async)
    - [get_body_json_async](#get_body_json_async)
    - [get_body_text_async](#get_body_text_async)
    - [send_body_bytes_async](#send_body_bytes_async)
    - [send_body_json_async](#send_body_json_async)
    - [send_body_text_async](#send_body_text_async)
    - [set_body_bytes](#set_body_bytes)
    - [set_body_json](#set_body_json)
    - [set_body_text](#set_body_text)

## bind_body_bytes_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L134)

```python
def bind_body_bytes_async(
    func: Callable[[HTTPContext], Future[Safe[bytes]]],
) -> HTTPHandler:
```

`HTTPHandler` that sets `bytes` processed from `func` execution.

#### Arguments

func (Callable[[HTTPContext], Future[Safe[bytes]]]): sync or async func that
produces error-safe `bytes`.

#### See also

- [HTTPContext](../core.md#httpcontext)
- [HTTPHandler](core.md#httphandler)

## bind_body_json_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L180)

```python
def bind_body_json_async(
    func: Callable[[HTTPContext], Future[Safe[BaseModel]]],
) -> HTTPHandler:
```

`HTTPHandler` that sets `BaseModel` processed from `func` execution.

#### Arguments

func (Callable[[HTTPContext], Future[Safe[BaseModel]]]): sync or async func that
produces error-safe `BaseModel`.

#### See also

- [HTTPContext](../core.md#httpcontext)
- [HTTPHandler](core.md#httphandler)

## bind_body_text_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L157)

```python
def bind_body_text_async(
    func: Callable[[HTTPContext], Future[Safe[str]]],
) -> HTTPHandler:
```

`HTTPHandler` that sets `str` processed from `func` execution.

#### Arguments

func (Callable[[HTTPContext], Future[Safe[str]]]): sync or async func that
produces error-safe `str`.

#### See also

- [HTTPContext](../core.md#httpcontext)
- [HTTPHandler](core.md#httphandler)

## get_body_bytes_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L18)

```python
def get_body_bytes_async(ctx: HTTPContext) -> Future[Safe[bytes]]:
```

Try to get `HTTPRequest` body as raw `bytes`.

If request body was not received than it will be. Than it will be extracted as
`Safe` from `HTTPContext`. Due to asynchronous nature of `receive_body` result is
some `Future`.

#### Arguments

- `ctx` *HTTPContext* - to try to get body from.

#### Returns

- `Future[Safe[bytes]]` - async result.

#### See also

- [HTTPContext](../core.md#httpcontext)

## get_body_json_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L56)

```python
def get_body_json_async(
    target_type: Type[BaseModel],
) -> Callable[[HTTPContext], Future[Safe[BaseModel]]]:
```

Parses `bytes` body as JSON to passed type and returns that from context.

Powered by `pydantic` `BaseModel`.

#### Notes

* https://pydantic-docs.helpmanual.io/

#### Arguments

- `target_type` *Type[BaseModel]* - to deserialize to.

#### Returns

- `Callable[[HTTPContext],` *Future[Safe[BaseModel]]]* - body getter.

#### See also

- [HTTPContext](../core.md#httpcontext)

## get_body_text_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L38)

```python
def get_body_text_async(ctx: HTTPContext) -> Future[Safe[str]]:
```

Try to get `HTTPRequest` body as `str`.

Gets body as `bytes` first and than decode as UTF-8.

#### Arguments

- `ctx` *HTTPContext* - to try to get body from.

#### Returns

- `Future[Safe[str]]` - async result.

#### See also

- [HTTPContext](../core.md#httpcontext)

## send_body_bytes_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L203)

```python
def send_body_bytes_async(data: bytes) -> HTTPHandler:
```

`HTTPHandler` that sets body to passed `bytes` and sends the response.

Also sets headers:
* Content-Length: XXX

#### Arguments

- `data` *bytes* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)

## send_body_json_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L234)

```python
def send_body_json_async(data: BaseModel) -> HTTPHandler:
```

`HTTPHandler` that sets body to passed `BaseModel` as json and sends response.

Also sets headers:
* Content-Type: application/json
* Content-Length: XXX

#### Arguments

- `data` *BaseModel* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)

## send_body_text_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L218)

```python
def send_body_text_async(data: str) -> HTTPHandler:
```

`HTTPHandler` that sets body to passed `str` and sends the response.

Also sets headers:
* Content-Type: text/plain
* Content-Length: XXX

#### Arguments

- `data` *str* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)

## set_body_bytes

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L83)

```python
def set_body_bytes(data: bytes) -> HTTPHandler:
```

`HTTPContext` handler that sets passed `bytes` to `HTTPResponse` body.

Also sets headers:
* Content-Length: XXX

#### Arguments

- `data` *bytes* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)

## set_body_json

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L118)

```python
def set_body_json(data: BaseModel) -> HTTPHandler:
```

`HTTPHandler` that sets passed `BaseModel` as json body of `HTTPResponse`.

Also sets headers:
* Content-Type: application/json
* Content-Length: XXX

#### Arguments

- `data` *BaseModel* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)

## set_body_text

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/body.py#L102)

```python
def set_body_text(data: str) -> HTTPHandler:
```

`HTTPContext` handler that sets passed `str` to `HTTPResponse` body.

Also sets headers:
* Content-Type: text/plain
* Content-Length: XXX

#### Arguments

- `data` *str* - to set as response body.

#### See also

- [HTTPHandler](core.md#httphandler)
