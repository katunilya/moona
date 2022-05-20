# Request Method

> Auto-generated documentation for [moona.http.request_method](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py) module.

- [Moona](../../README.md#-moona) / [Modules](../../MODULES.md#moona-modules) / [Moona](../index.md#moona) / [Http](index.md#http) / Request Method
    - [CONNECT](#connect)
    - [DELETE](#delete)
    - [GET](#get)
    - [HEAD](#head)
    - [OPTIONS](#options)
    - [PATCH](#patch)
    - [POST](#post)
    - [PUT](#put)
    - [TRACE](#trace)
    - [method](#method)

## CONNECT

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L116)

```python
@handler
def CONNECT(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with CONNECT method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## DELETE

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L72)

```python
@handler
def DELETE(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with DELETE method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## GET

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L28)

```python
@handler
def GET(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with GET method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## HEAD

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L94)

```python
@handler
def HEAD(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with HEAD method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## OPTIONS

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L83)

```python
@handler
def OPTIONS(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with OPTIONS method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## PATCH

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L50)

```python
@handler
def PATCH(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with PATCH method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## POST

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L39)

```python
@handler
def POST(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with POST method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## PUT

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L61)

```python
@handler
def PUT(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with PUT method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## TRACE

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L105)

```python
@handler
def TRACE(nxt: HTTPFunc, ctx: HTTPContext) -> Future[HTTPContext | None]:
```

Matches request with TRACE method.

#### Arguments

- `nxt` *HTTPFunc* - to run next.
- `ctx` *HTTPContext* - to process.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler](handlers.md#handler)

## method

[[find in source code]](https://github.com/katunilya/moona/blob/main/moona/http/request_method.py#L7)

```python
@handler1
def method(
    method: str,
    nxt: HTTPFunc,
    ctx: HTTPContext,
) -> Future[HTTPContext | None]:
```

Handler that matches request method with passed method.

When methods are equal pipeline is continued, otherwise skipped.

#### Arguments

- `method` *str* - method to match.
- `nxt` *HTTPFunc* - next func to run.
- `ctx` *HTTPContext* - to match with

#### Returns

Future[HTTPContext | None]: result.

#### See also

- [HTTPContext](context.md#httpcontext)
- [HTTPFunc](handlers.md#httpfunc)
- [handler1](handlers.md#handler1)
