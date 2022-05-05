# Events

> Auto-generated documentation for [mona.handlers.events](https://github.com/katunilya/mona/blob/main/mona/handlers/events.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Handlers](index.md#handlers) / Events
    - [receive_body_async](#receive_body_async)
    - [send_body_async](#send_body_async)
    - [send_response_start_async](#send_response_start_async)

## receive_body_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/events.py#L5)

```python
@http_handler
async def receive_body_async(ctx: HTTPContext) -> HTTPContextResult:
```

Handler "http.request" ASGI event, receive Request body.

If body was already taken, than nothing would be done and `Success` `HTTPContext`
would be returned. If at some point we receive "http.disconnect" event than
`HTTPContext` is closed and `Success` `HTTPContext` returned.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## send_body_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/events.py#L52)

```python
@http_handler
async def send_body_async(ctx: HTTPContext) -> HTTPContextResult:
```

Handler that sends "http.response.body" event to client.

If "http.response.start" event was not send than it will be during execution of this
handler.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)

## send_response_start_async

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/handlers/events.py#L34)

```python
@http_handler
async def send_response_start_async(ctx: HTTPContext) -> HTTPContextResult:
```

`HTTPContext` handler that sends "http.response.start" event to client.

#### See also

- [HTTPContextResult](core.md#httpcontextresult)
- [HTTPContext](../core.md#httpcontext)
- [http_handler](core.md#http_handler)
