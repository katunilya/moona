# Request Route

> Auto-generated documentation for [moona.http.request_route](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Request Route
    - [bind_params](#bind_params)
    - [bind_query](#bind_query)
    - [route](#route)
    - [route_ci](#route_ci)
    - [subroute](#subroute)
    - [subroute_ci](#subroute_ci)

## bind_params

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L105)

```python
def bind_params(path: str, func: Callable[..., HTTPHandler]) -> HTTPHandler:
```

Executes passed `func` on path params or skips pipeline.

#### Arguments

- `path` *str* - to match with.
func (Callable[..., HTTPHandler]): to run on request path params.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## bind_query

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L77)

```python
def bind_query(func: Callable[..., HTTPHandler]) -> HTTPHandler:
```

Executes passed `func` on path query.

#### Arguments

func (Callable[..., HTTPHandler]): to run on request path query.

#### See also

- [HTTPHandler](handlers.md#httphandler)

## route

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L10)

```python
@handler1
def route(
    path: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Handler that processes ctx only on right path.

Request path must be exactly the same as path passed as an argument to the handler
HOF. In order to keep them of the same format paths (bth in request and in handler)
are striped from leading and trailing "/".

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)

## route_ci

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L42)

```python
@handler1
def route_ci(
    path: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Handler that processes ctx only on right path.

Request path must be case-insensitive to path passed as an argument to the handler
HOF. In order to keep them of the same format paths (bth in request and in handler)
are striped from leading and trailing "/".

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)

## subroute

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L25)

```python
@handler1
def subroute(
    path: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Handler that proceeds only when Request path starts with passed path.

Leading part of the path is removed after processing the request. For example
request path was "group/users". Subroute waited for "group". After processing this
handler `HTTPContext` will have "users".

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)

## subroute_ci

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_route.py#L57)

```python
@handler1
def subroute_ci(
    path: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> future[HTTPContext | None]:
```

Handler that proceeds only when Request path starts with passed path.

Leading part of the path is removed after processing the request. For example
request path was "group/users". Subroute waited for "group". After processing this
handler `HTTPContext` will have "users". Route is case-insensitive.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)
