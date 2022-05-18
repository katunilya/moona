# Events

> Auto-generated documentation for [moona.http.events](https://github.com/katunilya/moona/blob/main/moona/http/events.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Events
    - [receive](#receive)
    - [respond](#respond)
    - [start](#start)

## receive

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/events.py#L50)

```python
@handler
async def receive(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
```

Receive request body from client.

#### Arguments

- `nxt` *HTTPFunc* - to execute next if body had been successfully received..
- `ctx` *HTTPContext* - to write body to.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## respond

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/events.py#L35)

```python
@handle_func
def respond(ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Send response body to the client and close the context.

#### Arguments

- `nxt` *HTTPFunc* - to execute next.
- `ctx` *HTTPContext* - context to send body from.

#### See also

- [HTTPContext](context.md#httpcontext)
- [handle_func](handlers.md#handle_func)

## start

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/events.py#L15)

```python
@handler
def start(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Send message to client and return `HTTPContext` that sent that.

#### Arguments

- `nxt` *HTTPHandler* - next handler.
- `ctx` *HTTPContext* - actor.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)
