# Context

> Auto-generated documentation for [mona.context](https://github.com/katunilya/mona/blob/main/mona/context.py) module.

- [Mona](../README.md#mona-index) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Context
    - [Client](#client)
    - [Context](#context)
    - [Request](#request)
    - [Response](#response)
    - [Server](#server)
    - [copy](#copy)
    - [from_asgi](#from_asgi)

## Client

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L16)

```python
dataclasses.dataclass
class Client():
```

Information about request client.

## Context

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L136)

```python
dataclasses.dataclass
class Context():
```

Wrapper for request data processing.

## Request

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L34)

```python
dataclasses.dataclass
class Request():
```

Immutable request data.

## Response

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L114)

```python
dataclasses.dataclass
class Response():
```

Request response data.

## Server

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L25)

```python
dataclasses.dataclass
class Server():
```

Information about server excepted request.

## copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L165)

```python
def copy(ctx: Context) -> Context:
```

Create [Context](#context) from another [Context](#context) as a copy.

#### Arguments

- `context` *Context* - to copy

#### Returns

- `Context` - copy

#### See also

- [Context](#context)

## from_asgi

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L146)

```python
def from_asgi(scope: Scope, receive: Receive, send: Send) -> Context:
```

Create context from ASGI function args.

#### Arguments

- `scope` *Scope* - ASGI scope
- `receive` *Receive* - ASGI receive
- `send` *Send* - ASGI send

#### Returns

- `Context` - for storing info about request

#### See also

- [Context](#context)
- [Receive](#receive)
- [Scope](#scope)
- [Send](#send)
