# State

> Auto-generated documentation for [mona.state](https://github.com/katunilya/mona/blob/main/mona/state.py) module.

- [Mona](../README.md#mona) / [Modules](../MODULES.md#mona-modules) / [Mona](index.md#mona) / State
    - [State](#state)
    - [accepts_error](#accepts_error)
    - [accepts_final](#accepts_final)
    - [accepts_right](#accepts_right)
    - [accepts_wrong](#accepts_wrong)
    - [accpets](#accpets)
    - [error](#error)
    - [final](#final)
    - [pack](#pack)
    - [rejects](#rejects)
    - [rejects_error](#rejects_error)
    - [rejects_final](#rejects_final)
    - [rejects_right](#rejects_right)
    - [rejects_wrong](#rejects_wrong)
    - [right](#right)
    - [switch_error](#switch_error)
    - [switch_final](#switch_final)
    - [switch_right](#switch_right)
    - [switch_wrong](#switch_wrong)
    - [unpack](#unpack)
    - [wrong](#wrong)

## State

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L15)

```python
dataclasses.dataclass(frozen=True)
class State(typing.Generic[T]):
```

Container for [State](#state)ful values.

#### See also

- [T](#t)

## accepts_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L228)

```python
def accepts_error(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on ERROR state.

#### See also

- [T](#t)
- [V](#v)

## accepts_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L240)

```python
def accepts_final(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on ERROR state.

#### See also

- [T](#t)
- [V](#v)

## accepts_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L204)

```python
def accepts_right(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on RIGHT state.

#### See also

- [T](#t)
- [V](#v)

## accepts_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L216)

```python
def accepts_wrong(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on WRONG state.

#### See also

- [T](#t)
- [V](#v)

## accpets

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L48)

```python
def accpets(
    state: typing.Any,
) -> typing.Callable[
    [
        typing.Callable[
            [
                T,
            ],
            V,
        ],
    ],
    typing.Callable[
        [
            State[T],
        ],
        State[V],
    ],
]:
```

Decorator that executes function only if state of container is `state`.

#### Arguments

- `state` *typing.Any* - target state

#### Returns

typing.Callable[
    [typing.Callable[[T], V]],
    - `typing.Callable[[State[T]],` *State[V]]]* - decorator

#### See also

- [T](#t)
- [V](#v)

## error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L132)

```python
def error(value: T) -> State[T]:
```

Wraps value into State container in ERROR state.

#### Arguments

- `value` *T* - to wrap

#### Returns

- `State[T]` - container

#### See also

- [T](#t)

## final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L144)

```python
def final(value: T) -> State[T]:
```

Wraps value into State container in FINAL state.

#### Arguments

- `value` *T* - to wrap

#### Returns

- `State[T]` - container

#### See also

- [T](#t)

## pack

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L22)

```python
@toolz.curry
def pack(state: typing.Any, value: T) -> State[T]:
```

Curried way of packing value into State container.

#### Arguments

- `state` *typing.Any* - to assign container
- `value` *T* - to wrap in container

#### Returns

- `State[T]` - container

#### See also

- [T](#t)

## rejects

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L74)

```python
def rejects(
    state: typing.Any,
) -> typing.Callable[
    [
        typing.Callable[
            [
                T,
            ],
            State[V],
        ],
    ],
    typing.Callable[
        [
            State[T],
        ],
        State[V],
    ],
]:
```

Decorator that executes function only if state of container is not `state`.

#### Arguments

- `state` *typing.Any* - target state

#### Returns

typing.Callable[
    [typing.Callable[[T], V]],
    - `typing.Callable[[State[T]],` *State[V]]]* - decorator

#### See also

- [T](#t)
- [V](#v)

## rejects_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L276)

```python
def rejects_error(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on not ERROR state.

#### See also

- [T](#t)
- [V](#v)

## rejects_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L288)

```python
def rejects_final(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on not ERROR state.

#### See also

- [T](#t)
- [V](#v)

## rejects_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L252)

```python
def rejects_right(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on not RIGHT state.

#### See also

- [T](#t)
- [V](#v)

## rejects_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L264)

```python
def rejects_wrong(
    function: typing.Callable[[T], State[V]],
) -> typing.Callable[[State[T]], State[V]]:
```

Function will be executed only on not WRONG state.

#### See also

- [T](#t)
- [V](#v)

## right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L108)

```python
def right(value: T) -> State[T]:
```

Wraps value into State container in RIGHT state.

#### Arguments

- `value` *T* - to wrap

#### Returns

- `State[T]` - container

#### See also

- [T](#t)

## switch_error

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L180)

```python
def switch_error(cnt: State[T]) -> State[T]:
```

Changes state of some container to ERROR.

#### Arguments

- `cnt` *State[T]* - to switch state

#### Returns

- `State[T]` - resulting state

#### See also

- [T](#t)

## switch_final

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L192)

```python
def switch_final(cnt: State[T]) -> State[T]:
```

Changes state of some container to FINAL.

#### Arguments

- `cnt` *State[T]* - to switch state

#### Returns

- `State[T]` - resulting state

#### See also

- [T](#t)

## switch_right

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L156)

```python
def switch_right(cnt: State[T]) -> State[T]:
```

Changes state of some container to RIGHT.

#### Arguments

- `cnt` *State[T]* - to switch state

#### Returns

- `State[T]` - resulting state

#### See also

- [T](#t)

## switch_wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L168)

```python
def switch_wrong(cnt: State[T]) -> State[T]:
```

Changes state of some container to WRONG.

#### Arguments

- `cnt` *State[T]* - to switch state

#### Returns

- `State[T]` - resulting state

#### See also

- [T](#t)

## unpack

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L36)

```python
def unpack(cnt: State[T]) -> T:
```

Extract value from State container.

#### Arguments

- `cnt` *State[T]* - container

#### Returns

- `T` - value

#### See also

- [T](#t)

## wrong

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/state.py#L120)

```python
def wrong(value: T) -> State[T]:
```

Wraps value into State container in WRONG state.

#### Arguments

- `value` *T* - to wrap

#### Returns

- `State[T]` - container

#### See also

- [T](#t)
