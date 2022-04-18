# State

> Auto-generated documentation for [mona.state](https://github.com/katunilya/mona/blob/main/mona/state.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / State
    - [Error](#error)
    - [Final](#final)
    - [Right](#right)
    - [State](#state)
        - [State().\_\_rshift\_\_](#state__rshift__)
    - [Wrong](#wrong)
    - [accepts_error](#accepts_error)
    - [accepts_final](#accepts_final)
    - [accepts_right](#accepts_right)
    - [accepts_wrong](#accepts_wrong)
    - [rejects_error](#rejects_error)
    - [rejects_final](#rejects_final)
    - [rejects_right](#rejects_right)
    - [rejects_wrong](#rejects_wrong)
    - [switch_to_error](#switch_to_error)
    - [switch_to_final](#switch_to_final)
    - [switch_to_right](#switch_to_right)
    - [switch_to_wrong](#switch_to_wrong)
    - [unpacks](#unpacks)

## Error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L35)

```python
dataclasses.dataclass(frozen=True)
class Error(State[TError]):
```

Value should not be processed next due to error.

#### See also

- [TError](#terror)

## Final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L40)

```python
dataclasses.dataclass(frozen=True)
class Final(State[T]):
```

Value should not be processed next as processing finished.

#### See also

- [T](#t)

## Right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L25)

```python
dataclasses.dataclass(frozen=True)
class Right(State[T]):
```

Value should be processed next.

#### See also

- [T](#t)

## State

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L12)

```python
dataclasses.dataclass(frozen=True)
class State(abc.ABC, typing.Generic[T]):
```

Base container for Statefull values.

#### See also

- [T](#t)

### State().\_\_rshift\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L17)

```python
def __rshift__(
    function: typing.Callable[['State[T]'], 'State[V]'],
) -> 'State[V]':
```

Dunder function for >> syntax of executing statefull functions.

## Wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L30)

```python
dataclasses.dataclass(frozen=True)
class Wrong(State[T]):
```

Value should not be processed next.

#### See also

- [T](#t)

## accepts_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L88)

```python
def accepts_error(function: typing.Callable[[T], State[V]]):
```

Decorator that executes guarded function only when monad is in FINAL state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## accepts_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L105)

```python
def accepts_final(function: typing.Callable[[T], State[V]]):
```

Decorator that executes guarded function only when monad is in FINAL state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## accepts_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L54)

```python
def accepts_right(function: typing.Callable[[T], State[V]]):
```

Decorator that executes guarded function only when monad is in RIGHT state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## accepts_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L71)

```python
def accepts_wrong(function: typing.Callable[[T], State[V]]):
```

Decorator that executes guarded function only when monad is in WRONG state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## rejects_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L156)

```python
def rejects_error(function: typing.Callable[[T], State[V]]):
```

Decorator that guards function from container in ERROR state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## rejects_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L173)

```python
def rejects_final(function: typing.Callable[[T], State[V]]):
```

Decorator that guards function from container in FINAL state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## rejects_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L122)

```python
def rejects_right(function: typing.Callable[[T], State[V]]):
```

Decorator that guards function from container in RIGHT state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## rejects_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L139)

```python
def rejects_wrong(function: typing.Callable[[T], State[V]]):
```

Decorator that guards function from container in WRONG state.

This decorator also unpacks [State](#state) container.

#### See also

- [T](#t)
- [V](#v)

## switch_to_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L214)

```python
def switch_to_error(s: State[T]) -> Error[T]:
```

Changes container for Statefull value to Error.

#### Arguments

- `s` *State[T]* - initial State container

#### Returns

- `Error[T]` - container

#### See also

- [T](#t)

## switch_to_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L226)

```python
def switch_to_final(s: State[T]) -> Right[T]:
```

Changes container for Statefull value to Final.

#### Arguments

- `s` *State[T]* - initial State container

#### Returns

- `Final[T]` - container

#### See also

- [T](#t)

## switch_to_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L190)

```python
def switch_to_right(s: State[T]) -> Right[T]:
```

Changes container for Statefull value to Right.

#### Arguments

- `s` *State[T]* - initial State container

#### Returns

- `Right[T]` - container

#### See also

- [T](#t)

## switch_to_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L202)

```python
def switch_to_wrong(s: State[T]) -> Wrong[T]:
```

Changes container for Statefull value to Wrong.

#### Arguments

- `s` *State[T]* - initial State container

#### Returns

- `Wrong[T]` - container

#### See also

- [T](#t)

## unpacks

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L44)

```python
def unpacks(function: typing.Callable[[T], State[V]]):
```

Decorator for automatic unpacking of State for function execution.

#### See also

- [T](#t)
- [V](#v)
