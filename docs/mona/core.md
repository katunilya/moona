# Core

> Auto-generated documentation for [mona.core](https://github.com/katunilya/mona/blob/main/mona/core.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Core
    - [BaseContext](#basecontext)
        - [BaseContext().\_\_rshift\_\_](#basecontext__rshift__)
        - [BaseContext().copy](#basecontextcopy)
    - [ClientInfo](#clientinfo)
    - [ContextError](#contexterror)
    - [HTTPContext](#httpcontext)
        - [HTTPContext().copy](#httpcontextcopy)
        - [HTTPContext.create](#httpcontextcreate)
    - [HTTPRequest](#httprequest)
        - [HTTPRequest().copy](#httprequestcopy)
        - [HTTPRequest.create](#httprequestcreate)
    - [HTTPResponse](#httpresponse)
        - [HTTPResponse().copy](#httpresponsecopy)
        - [HTTPResponse.empty](#httpresponseempty)
    - [LifespanContext](#lifespancontext)
        - [LifespanContext().copy](#lifespancontextcopy)
        - [LifespanContext.create](#lifespancontextcreate)
    - [ServerInfo](#serverinfo)

## BaseContext

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L19)

```python
class BaseContext(ABC, Bindable):
```

Base class for each kind of Context handled by application.

Mainly there are 3 kinds:
* [HTTPContext](#httpcontext) for "http" request scopes
* [LifespanContext](#lifespancontext) for "lifetime" request scopes
* `WebsocketContext` (not implemented)

#### See also

- [Bindable](monads/core.md#bindable)

### BaseContext().\_\_rshift\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L28)

```python
def __rshift__(
    handler: Callable[
        [
            BaseContext | ContextError,
        ],
        BaseContext | ContextError | Awaitable[BaseContext | ContextError],
    ],
) -> BaseContext | ContextError | Awaitable[BaseContext | ContextError]:
```

Binding for [BaseContext](#basecontext).

Remember that for piplines with async handlers one must use `Future`.

#### Arguments

handler (Callable[[BaseContext | ContextError], BaseContext | ContextError |
Awaitable[BaseContext | ContextError]]): sync handler to execute with this
ctx.

#### Returns

BaseContext | ContextError | Awaitable[BaseContext | ContextError]: result
of handler.

### BaseContext().copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L50)

```python
@abstractmethod
def copy() -> BaseContext:
```

Creates deepcopy of the context.

## ClientInfo

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L120)

```python
dataclass
class ClientInfo():
```

Information related to client that sent the request.

Based on ASGI specification client in HTTP and Websocket connection scope is a pair
of host and port where host is IPv4 or IPv6 address or unix socketand port is remote
port integer. Port is optional.

#### Notes

Websockets are not supported.

## ContextError

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L386)

```python
class ContextError(Exception, BaseContext):
    def __init__(
        ctx: BaseContext,
        message: str = 'Internal Server Error.',
        status=500,
    ) -> None:
```

Base class for `Exception`s that happen during handling [HTTPContext](#httpcontext).

#### Attributes

- `ctx` *HTTPContext* - context that failed to be processed.
- `message` *str* - message to respond.
- `status` *int* - status code for response to send.

#### Arguments

- `ctx` *HTTPContext* - context that failed to be processed.
- `message` *str* - message to respond.
- `status` *int* - status code for response to send.

#### See also

- [BaseContext](#basecontext)

## HTTPContext

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L318)

```python
dataclass
class HTTPContext(BaseContext):
```

Object that contains entire information related to HTTP Request.

Mostly it's structure is replication of HTTP Connection Scope of ASGI Specification.
It contains information on both request and response and also functions for sending
and receiving information.

#### Notes

https://asgi.readthedocs.io/en/latest/specs/www.html#

#### Attributes

- `request` *HTTPRequest* - information received by the server. response
- `(HTTPResponse)` - information that should be sent by the server.
- `receive` *Receive* - function for acquiring events from client. send (Send):
function for sending events to the client.
- `started` *bool* - flag that defines if response has started.
- `closed` *bool* - flag that defines if connection is closed due to Timeout from
user or request finish.

#### See also

- [BaseContext](#basecontext)

### HTTPContext().copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L365)

```python
def copy() -> HTTPContext:
```

Create complete copy of [HTTPContext](#httpcontext).

This function is needed to avoid side effects due to reference nature of Python
when using `choose` combinator.

#### Returns

- `HTTPContext` - deepcopy if [HTTPContext](#httpcontext).

### HTTPContext.create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L346)

```python
@staticmethod
def create(scope: Scope, receive: Receive, send: Send) -> HTTPContext:
```

Create context from ASGI function args.

#### Arguments

- `scope` *Scope* - ASGI scope.
- `receive` *Receive* - ASGI receive.
- `send` *Send* - ASGI send.

#### Returns

- `HTTPContext` - for storing info about request.

#### See also

- [Receive](#receive)
- [Scope](#scope)
- [Send](#send)

## HTTPRequest

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L152)

```python
dataclass
class HTTPRequest():
```

Information related to HTTP request from ASGI Connection Scope object.

Object that contains information related to HTTP Request based on ASGI
specification.

#### Notes

https://asgi.readthedocs.io/en/latest/specs/www.html#

#### Attributes

- `type_` *str* - "http" or "websocket" string which specifies kind of request.
- `method` *str* - HTTP method name, uppercased.
- `asgi_version` *str* - version of the ASGI spec.
- `asgi_spec_version` *str* - version of the ASGI HTTP spec this server understands;
one of "2.0", "2.1", "2.2" or "2.3". Optional; if missing assume "2.0".
- `http_version` *str* - one of "1.1" or "2". Optional; if missing default is "1.1".
- `scheme` *str* - URL scheme portion (likely "http" or "https"). Optional (but must
not be empty); Defaults to "http".
- `path` *str* - HTTP request target excluding any query string, with percent-encoded
sequences and UTF-8 byte sequences decoded into characters.
- `query_string` *bytes* - URL portion after the ?, percent-encoded.
headers (dict[str, str]): dictionary for request headers.
body (bytes | None): request body. `None` by default.
- `server` *ServerInfo* - information about server received request.
- `client` *ClientInfo* - information about client sent the request.

### HTTPRequest().copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L244)

```python
def copy() -> HTTPRequest:
```

Create a deepcopy of [HTTPRequest](#httprequest).

#### Returns

- `HTTPRequest` - deepcopy.

### HTTPRequest.create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L207)

```python
@staticmethod
def create(scope: Scope) -> HTTPRequest:
```

Create [HTTPRequest](#httprequest) object from ASGI scope.

#### Arguments

- `scope` *Scope* - ASGI scope.

#### Returns

- `HTTPRequest` - result.

#### See also

- [Scope](#scope)

## HTTPResponse

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L267)

```python
dataclass
class HTTPResponse():
```

Information related to HTTP Response sent by the application.

Response contains both information for Response Start send event and Response Body
send event.

#### Attributes

- `status` *int* - response status code. Defaults to 200 (SUCCESS).
headers (dict[str, str]): dictionary of response headers. Defaults to dict().
body (bytes | None): response body. Defaults to b''.

### HTTPResponse().copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L304)

```python
def copy() -> HTTPResponse:
```

Create a deepcopy of [HTTPResponse](#httpresponse).

#### Returns

- `HTTPResponse` - deepcopy of [HTTPResponse](#httpresponse).

### HTTPResponse.empty

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L288)

```python
@staticmethod
def empty() -> HTTPResponse:
```

Create empty [HTTPResponse](#httpresponse).

Empty [HTTPResponse](#httpresponse) has 200 OK status code, empty dictionary for headers and
empty bytes string for body.

#### Returns

- `HTTPResponse` - empty response.

## LifespanContext

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L57)

```python
dataclass
class LifespanContext(BaseContext):
```

Context for handling actions performed on startup and shutdown.

It contains all the information required based on ASGI Lifespan Specification.

#### Notes

https://asgi.readthedocs.io/en/latest/specs/lifespan.html

#### Attributes

- `type_` *str* - type of context. Must be "lifespan".
- `asgi_version` *str* - version of the ASGI spec.
- `asgi_spec_version` *str* - The version of this spec being used. Optional; if
missing defaults to "1.0".
- `receive` *Receive* - ASGI receive function.
- `send` *Send* - ASGI send function.

#### See also

- [BaseContext](#basecontext)

### LifespanContext().copy

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L100)

```python
def copy() -> LifespanContext:
```

Create a deepcopy of [LifespanContext](#lifespancontext).

This handler is needed for `choose` combinator. Without it side-effects might
put context in some broken state.

#### Returns

- `LifespanContext` - deepcopy.

### LifespanContext.create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L80)

```python
@staticmethod
def create(scope: Scope, receive: Receive, send: Send) -> LifespanContext:
```

Creates an instance of [LifespanContext](#lifespancontext) from ASGI args.

#### Arguments

- `scope` *Scope* - ASGI scope.
- `receive` *Receive* - ASGI receive function.
- `send` *Send* - ASGI send function.

#### Returns

- `LifespanContext` - result.

#### See also

- [Receive](#receive)
- [Scope](#scope)
- [Send](#send)

## ServerInfo

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/core.py#L136)

```python
dataclass
class ServerInfo():
```

Information related to server that received the request.

Based on ASGI specification server in HTTP and Websocket connection scope is a pair
of host and port where host is the listening address or unix socket for this server
and port is the interger listening port. Port is optional.

#### Notes

Websockets are not supported.
