# Maybe

> Auto-generated documentation for [mona.monads.maybe](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Monads](index.md#monads) / Maybe
    - [Maybe](#maybe)
        - [Maybe.altered](#maybealtered)
        - [Maybe.bound](#maybebound)
        - [Maybe.choose](#maybechoose)
        - [Maybe.noneless](#maybenoneless)
        - [Maybe.nothing](#maybenothing)
        - [Maybe.some](#maybesome)
    - [Nothing](#nothing)
    - [Some](#some)

## Maybe

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L15)

```python
dataclass(frozen=True)
class Maybe(Bindable, Alterable, Generic[TSome], ABC):
```

General purpose container for optional value.

[Maybe](#maybe) container has 2 variations: [Some](#some) and [Nothing](#nothing). [Some](#some) stands for some
actual value and means that it is present in execution context. [Nothing](#nothing) on the
other hand describes emtpiness and lack of value. This is additional wrapping around
`None` values.

Example

```python
user = {
    "name": "John Doe"
    "emails": {
        "primary_email": "john_doe@example.com",
    }
}

primary_email = (
    Some(user)
    >> get("emails"),
    >> get("primary_email")
    << or_empty_str
)  # Some("john_doe@example.com")

primary_email = (
    Some(user)
    >> get("emails"),
    >> get("secondary_email")  # Nothing appeared here!
    << or_empty_str
)  # Some("")
```

#### See also

- [Alterable](core.md#alterable)
- [Bindable](core.md#bindable)
- [TSome](#tsome)

### Maybe.altered

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L86)

```python
@staticmethod
def altered(
    func: Callable[[TSome], 'Maybe[VSome]'],
) -> Callable[['Maybe[TSome]'], 'Maybe[VSome]']:
```

Decorator for functions that will be executed only with [Nothing](#nothing).

Changes input type to [Maybe](#maybe).

Example

```python
@Maybe.altered
def or_zero(_) -> Maybe[int]:
    return Some(0)

or_zero(Nothing())  # Some(0)
```

#### See also

- [TSome](#tsome)

### Maybe.bound

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L63)

```python
@staticmethod
def bound(
    func: Callable[[TSome], 'Maybe[VSome]'],
) -> Callable[['Maybe[TSome]'], 'Maybe[VSome]']:
```

Decorator for functions that will be executed only with [Some](#some) value.

Changes input type to [Maybe](#maybe).

Example

```python
@Maybe.bound
def get_user(name: str) -> Maybe[User]:
    ...

result get_user(Nothing())  # Nothing
```

#### See also

- [TSome](#tsome)

### Maybe.choose

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L122)

```python
@staticmethod
def choose(*funcs: Callable[[TSome], VSome]) -> Callable[[TSome], VSome]:
```

Return first [Some](#some) result from passed functions.

If `funcs` is empty, than return [Nothing](#nothing).
If no `func` can return [Some](#some) than return [Nothing](#nothing).

Example

```python
result = Some(1) >> choose(
    lambda x: Nothing(),
    lambda x: Some(2)
)  # Some(2)
```

#### See also

- [TSome](#tsome)
- [VSome](#vsome)

### Maybe.noneless

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L146)

```python
@staticmethod
def noneless(
    func: Callable[[TSome], VSome | None],
) -> Callable[[TSome], 'Maybe[VSome]']:
```

Decorator for functions that might return `None`.

When decorated function returns `None` it is converted to [Nothing](#nothing), otherwise
wrapped into [Some](#some) container.

Example

```python
@Maybe.noneless
def func(x: int) -> int | None:
    return x if x > 10 else None

Some(1) >> func  # Nothing
```

#### See also

- [TSome](#tsome)

### Maybe.nothing

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L186)

```python
@staticmethod
def nothing(_: Any) -> Nothing:
```

Converts `Any` value into nothing.

#### Returns

- `Nothing` - container.

#### See also

- [Nothing](#nothing)

### Maybe.some

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L174)

```python
@staticmethod
def some(value: TSome) -> Some[TSome]:
```

Wraps passed value into [Some](#some) container.

#### Arguments

- `value` *TSome* - to wrap.

#### Returns

- `Some[TSome]` - container.

#### See also

- [TSome](#tsome)

## Nothing

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L202)

```python
dataclass(frozen=True)
class Nothing(Maybe[Any]):
    def __init__() -> None:
```

Singleton [Maybe](#maybe) container marking value absence.

## Some

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/maybe.py#L197)

```python
dataclass(frozen=True)
class Some(Maybe[TSome]):
```

[Maybe](#maybe) container for values that are actually present.

#### See also

- [TSome](#tsome)
