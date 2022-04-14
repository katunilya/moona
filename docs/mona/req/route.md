# Route

> Auto-generated documentation for [mona.req.route](https://github.com/katunilya/mona/blob/main/mona/req/route.py) module.

- [Mona](../../README.md#mona-index) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Req](index.md#req) / Route
    - [on_ciroute](#on_ciroute)
    - [on_cisubroute](#on_cisubroute)
    - [on_route](#on_route)
    - [on_subroute](#on_subroute)

## on_ciroute

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/route.py#L31)

```python
def on_ciroute(pattern: str) -> handler.Handler:
```

Case insensitive version of [on_route](#on_route).

## on_cisubroute

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/route.py#L46)

```python
def on_cisubroute(pattern: str) -> handler.Handler:
```

Case insensitive version of [on_subroute](#on_subroute).

## on_route

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/route.py#L4)

```python
def on_route(pattern: str) -> handler.Handler:
```

If request `path` is the same as `pattern` than context is valid.

## on_subroute

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/req/route.py#L15)

```python
def on_subroute(pattern: str) -> handler.Handler:
```

Returns valid context without subroute part of it if `pattern` equals `path`.
