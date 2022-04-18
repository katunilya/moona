# Context

> Auto-generated documentation for [mona.context](https://github.com/katunilya/mona/blob/main/mona/context.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Context
    - [Client](#client)
    - [Context](#context)
    - [Request](#request)
    - [Response](#response)
    - [Server](#server)
    - [copy](#copy)
    - [from_asgi](#from_asgi)

## Client

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L17)

```python
dataclasses.dataclass
class Client():
```

Information about request client.

## Context

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L145)

```python
dataclasses.dataclass
class Context():
```

Wrapper for request data processing.

## Request

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L35)

```python
dataclasses.dataclass
class Request():
```

Immutable request data.

## Response

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L123)

```python
dataclasses.dataclass
class Response():
```

Request response data.

## Server

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L26)

```python
dataclasses.dataclass
class Server():
```

Information about server excepted request.

## copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L175)

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

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/context.py#L155)

```python
def from_asgi(asgi: ASGIData) -> Context:
```

Create context from ASGI function args.

#### Arguments

- `scope` *Scope* - ASGI scope
- `receive` *Receive* - ASGI receive
- `send` *Send* - ASGI send

#### Returns

- `Context` - for storing info about request

#### See also

- [ASGIData](#asgidata)
- [Context](#context)
