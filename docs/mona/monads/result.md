# Result

> Auto-generated documentation for [mona.monads.result](https://github.com/katunilya/mona/blob/main/mona/monads/result.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Monads](index.md#monads) / Result
    - [Failure](#failure)
    - [Result](#result)
        - [Result.altered](#resultaltered)
        - [Result.bound](#resultbound)
        - [Result.failed](#resultfailed)
        - [Result.safe](#resultsafe)
        - [Result.safely_bound](#resultsafely_bound)
        - [Result.successfull](#resultsuccessfull)
    - [Success](#success)

## Failure

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L179)

```python
dataclass(frozen=True)
class Failure(Result[Any, TFailure]):
```

Container that marks underlying value as [Failure](#failure) execution result.

#### See also

- [TFailure](#tfailure)

## Result

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L17)

```python
dataclass(frozen=True)
class Result(Bindable, Alterable, Generic[TSuccess, TFailure], ABC):
```

Base abstract container for computation [Result](#result).

Railway-oriented programming concept. Stands for [Result](#result) of some computation
sequence. Can be of 2 types: [Success](#success) and [Failure](#failure).

Example

```python
def make_moderator_admin(id: int) -> Result[User, Exception]:
    return (
        get_user(id)
        >> check_user_role_is('moderator')
        >> set_user_role('admin')
        >> update_user
    )
```

#### See also

- [Alterable](core.md#alterable)
- [Bindable](core.md#bindable)
- [TFailure](#tfailure)
- [TSuccess](#tsuccess)

### Result.altered

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L78)

```python
@staticmethod
def altered(
    func: Callable[[TFailure], 'Result[VSuccess, VFailure]'],
) -> Callable[['Result[TSuccess, TFailure]'], 'Result[VSuccess, VFailure]']:
```

Decorator for functions that will be executed only with [Failure](#failure) [Result](#result).

Changes input and output types for passed function to [Result](#result).

Example

```python
@Result.bindable
def handle_error(err: Exception) -> str:
    ...

result = handle_error(Failure(Exception(..)))  # Success[str]
```

#### See also

- [TFailure](#tfailure)

### Result.bound

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L55)

```python
@staticmethod
def bound(
    func: Callable[[TSuccess], 'Result[VSuccess, VFailure]'],
) -> Callable[['Result[TSuccess, TFailure]'], 'Result[VSuccess, VFailure]']:
```

Decorator for functions that will be executed only with [Success](#success) [Result](#result).

Changes input and output types for passed function to [Result](#result).

Example

```python
@Result.bindable
def check_is_admin(user: User) -> User:
    ...

result = check_is_admin(Success(User(..)))  # Result[User, Exception]
```

#### See also

- [TSuccess](#tsuccess)

### Result.failed

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L151)

```python
@staticmethod
def failed(value: TFailure) -> Failure[TFailure]:
```

Wraps passed value into Failure container.

#### Arguments

- `value` *TFailure* - value to wrap.

#### Returns

- `Failure[TFailure]` - container.

#### See also

- [TFailure](#tfailure)

### Result.safe

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L101)

```python
@staticmethod
def safe(
    func: Callable[[TSuccess], VSuccess | Exception],
) -> Callable[[TSuccess], Result[VSuccess, Exception]]:
```

When function returns or throws `Exception` it is wrapped into [Failure](#failure).

Example

```python
@Result.safe
def divide_one_by(x: int) -> int:
    return 1 / x

divide_one_by(0)  # Failure(value=ZeroDivisionError('division by zero'))

@Result.safe
def divide_two_by(x: int) -> int | Exception:
    match x:
        case 0:
            return ValueError('Cannot divide by zero')
        case value:
            return 2 / value

divide_two_by(0)  # Failure(value=ValueError('Cannot divide by zero'))
```

#### See also

- [TSuccess](#tsuccess)
- [VSuccess](#vsuccess)

### Result.safely_bound

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L163)

```python
@staticmethod
def safely_bound(
    func: Callable[[TSuccess], VSuccess | Exception],
) -> Callable[[Result[TSuccess, TFailure]], Result[VSuccess, Exception]]:
```

Decorator for functions that combines [Result.bound](#resultbound) and [Result.safe](#resultsafe).

#### See also

- [TFailure](#tfailure)
- [TSuccess](#tsuccess)
- [VSuccess](#vsuccess)

### Result.successfull

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L139)

```python
@staticmethod
def successfull(value: TSuccess) -> Success[TSuccess]:
```

Wraps passed value into Success container.

#### Arguments

- `value` *TSuccess* - value to wrap.

#### Returns

- `Success[TSuccess]` - container.

#### See also

- [TSuccess](#tsuccess)

## Success

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/result.py#L172)

```python
dataclass(frozen=True)
class Success(Result[TSuccess, Any]):
```

Container that marks underlying value as [Success](#success)full execution result.

#### See also

- [TSuccess](#tsuccess)
