# Core

> Auto-generated documentation for [mona.monads.core](https://github.com/katunilya/mona/blob/main/mona/monads/core.py) module.

- [Mona](../../README.md#mona) / [Modules](../../MODULES.md#mona-modules) / [Mona](../index.md#mona) / [Monads](index.md#monads) / Core
    - [Alterable](#alterable)
        - [Alterable().\_\_lshift\_\_](#alterable__lshift__)
    - [Bindable](#bindable)
        - [Bindable().\_\_rshift\_\_](#bindable__rshift__)

## Alterable

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/core.py#L20)

```python
class Alterable(Protocol):
```

Interface for monad containers that support altering.

Altering is application of passed function on some monad-specific pre-condition or
action. Altering is done via `<<` operator. Commonly altering is applied only when
container is in some "wrong" state and computation cannot be continued. Opposite of
binding.

### Alterable().\_\_lshift\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/core.py#L29)

```python
def __lshift__(func: Callable):
```

Dunder method for `func` altering.

#### Arguments

- `func` *Callable* - function to alter.

## Bindable

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/core.py#L4)

```python
class Bindable(Protocol):
```

Interface for monad containers that support binding.

Binding is application of passed function on some monad-specific pre-condition or
action. Binding is done via `>>` operator. Commonly binding is applied only when
container is in some "right" state and computation can be continued.

### Bindable().\_\_rshift\_\_

[[find in source code]](https://github.com/katunilya/mona/blob/main/mona/monads/core.py#L12)

```python
def __rshift__(func: Callable):
```

Dunder method for `func` binding.

#### Arguments

- `func` *Callable* - function to bind.
