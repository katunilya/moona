# Future

> Auto-generated documentation for [mona.monads.future](https://github.com/katunilya/mona/blob/main/mona/monads/future.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Monads](index.md#monads) / Future
    - [Future](#future)
        - [Future.bound](#futurebound)
        - [Future.compose](#futurecompose)
        - [Future.create](#futurecreate)
        - [Future.do](#futuredo)
        - [Future.identity](#futureidentity)

## Future

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L13)

```python
dataclass(frozen=True)
class Future(Bindable, Generic[T]):
```

Container for performing asynchronous operations on some value in sync context.

[Future](#future) allows running async function inside synchronous functions. Can execute
both sync and async functions and produce next [Future](#future)s.

Example

```python
f = (
    Future.create(3)
    >> (lambda x: x + 1)
    >> async_inc
    >> async_power_2
)  # Future (awaitable)
print(await f)  # 25
```

#### See also

- [Bindable](core.md#bindable)
- [T](#t)

### Future.bound

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L76)

```python
@staticmethod
def bound(
    func: Callable[[T], Awaitable[V] | V],
) -> Callable[['Future[T]'], 'Future[V]']:
```

Decorator for functions to make them work with `Futures`.

Makes function automatically bindable for [Future](#future) without `>>` syntax.

Example

```python
@Future.bound
def plus_1(x: int) -> int:
    return x + 1

plus_1(Future.create(3))  # Future(4)
```

#### See also

- [T](#t)

### Future.compose

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L99)

```python
@staticmethod
def compose(
    *funcs: Callable[[T], Awaitable[V] | V],
) -> Callable[[T], Awaitable[V]]:
```

Combinator for sync and async functions that converts them into async pipeline.

If `funcs` is empty than returns async identity function.

#### Examples

```python
composition = Future.compose(
    async_plus_1,
    sync_plus_1,
)  # asynchronous function that executes async_func, than sync_func

result = await (Future.create(3) >> composition)  # 5
```

#### Returns

- `Callable[[T],` *Awaitable[V]]* - function composition

#### See also

- [T](#t)
- [V](#v)

### Future.create

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L59)

```python
@staticmethod
def create(value: T) -> 'Future[T]':
```

Create future from some present value (not awaitable).

#### Examples

```python
f = Future.create(1)
print(await f)  # 1
```

#### Arguments

- `value` *T* - value to wrap into [Future](#future)

#### Returns

- `Future[T]` - result

#### See also

- [T](#t)

### Future.do

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L127)

```python
@staticmethod
def do(
    cnt: T | 'Future[T]',
    *funcs: Callable[[T], Awaitable[V] | V],
) -> 'Future[V]':
```

Execute multiple sync and async function on some [Future](#future) container.

Basically this is for running some pipeline on some value. Supports both sync
and [Future](#future) values. Sequentially executes functions one-by-one via composition.
Useful for cases when `funcs` are not known and come as first-class citizens and
must be executed. In case functions to run are know use `>>` syntax for more
readable pipeline execution syntax.

#### Examples

```python
f = Future.do(
    3,
    lambda x: x + 1,
    async_inc,
    async_power_2
)  # Future (awaitable)
print(await f)  # 25
```

#### Arguments

cnt (T | Future[T]): to use as argument for functions.

#### Returns

- `Future[V]` - result.

#### See also

- [T](#t)

### Future.identity

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/future.py#L42)

```python
@staticmethod
async def identity(value: T) -> T:
```

Asynchronously returns passed `value`.

#### Examples

```python
f = Future.identity(3)  # awaitable 3
print(await f)  # 3
```

#### Arguments

- `value` *T* - to return asynchronously

#### Returns

- `T` - return value

#### See also

- [T](#t)
