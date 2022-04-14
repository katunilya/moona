# Future

> Auto-generated documentation for [mona.future](https://github.com/katunilya/mona/blob/main/mona/future.py) module.

- [Mona](../README.md#mona-index) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / Future
    - [Future](#future)
        - [Future().\_\_await\_\_](#future__await__)
        - [Future().\_\_rshift\_\_](#future__rshift__)
    - [bind](#bind)
    - [compose](#compose)
    - [from_value](#from_value)
    - [identity](#identity)
    - [pipe](#pipe)

## Future

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L12)

```python
dataclasses.dataclass(frozen=True)
class Future(typing.Generic[T]):
```

Container for awaitable values.

#### See also

- [T](#t)

### Future().\_\_await\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L17)

```python
def __await__() -> typing.Generator[None, None, T]:
```

Dunder function that makes [Future](#future) awaitable.

#### See also

- [T](#t)

### Future().\_\_rshift\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L21)

```python
def __rshift__(
    function: typing.Callable[['Future[T]'], 'Future[V]'],
) -> 'Future[V]':
```

Dunder function for >> syntax of executing futures.

## bind

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L61)

```python
@toolz.curry
def bind(
    function: typing.Callable[[T], typing.Union[typing.Awaitable[V], V]],
    cnt: Future[T],
) -> Future[V]:
```

Bind sync or async function to Future.

#### Arguments

function (typing.Callable[[T], typing.Union[V, typing.Awaitable[V]]]): to bind
- `cnt` *Future[T]* - container

#### Returns

- `Future[V]` - result of running `function` on `cnt` value

#### See also

- [T](#t)
- [V](#v)

## compose

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L77)

```python
def compose(
    *functions: typing.Union[
        typing.Callable[
            [
                T,
            ],
            typing.Awaitable[V],
        ],
        typing.Callable[
            [
                T,
            ],
            V,
        ],
    ],
) -> typing.Callable[[T], typing.Awaitable[V]]:
```

Converts sequence of functions into sequenced pipeline for [Future](#future) container.

#### Returns

- `typing.Callable[[Future[T]],` *Future[V]]* - function composition

#### See also

- [T](#t)
- [V](#v)

## from_value

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L40)

```python
def from_value(value: T) -> Future[T]:
```

Create [Future](#future) from value.

Do not pass here another `Awaitable`.

#### Arguments

- `value` *T* - value to create awaitable.

#### Returns

- `Future[T]` - ready-to-use future

#### See also

- [T](#t)

## identity

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L28)

```python
async def identity(value: T) -> T:
```

Converts some value into Awaitable.

#### Arguments

- `value` *T* - to be converted to awaitable.

#### Returns

- `T` - awaitable value

#### See also

- [T](#t)

## pipe

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/future.py#L98)

```python
def pipe(
    cnt: Future[T],
    *functions: typing.Union[
        typing.Callable[
            [
                T,
            ],
            typing.Awaitable[V],
        ],
        typing.Callable[
            [
                T,
            ],
            V,
        ],
    ],
) -> Future[V]:
```

Composes `functions` and executes on `cnt`.

#### Arguments

- `cnt` *Future[T]* - to execute

#### Returns

- `Future[V]` - result future

#### See also

- [T](#t)
- [V](#v)
