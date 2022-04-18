import abc
import dataclasses
import functools
import typing

T = typing.TypeVar("T")
V = typing.TypeVar("V")
TError = typing.TypeVar("TError", bound=Exception)


@dataclasses.dataclass(frozen=True)
class State(abc.ABC, typing.Generic[T]):
    """Base container for Statefull values."""

    value: T

    def __rshift__(
        self, function: typing.Callable[["State[T]"], "State[V]"]
    ) -> "State[V]":
        """Dunder function for >> syntax of executing statefull functions."""
        return function(self)


@dataclasses.dataclass(frozen=True)
class Right(State[T]):
    """Value should be processed next."""


@dataclasses.dataclass(frozen=True)
class Wrong(State[T]):
    """Value should not be processed next."""


@dataclasses.dataclass(frozen=True)
class Error(State[TError]):
    """Value should not be processed next due to error."""


@dataclasses.dataclass(frozen=True)
class Final(State[T]):
    """Value should not be processed next as processing finished."""


def unpacks(function: typing.Callable[[T], State[V]]):
    """Decorator for automatic unpacking of State for function execution."""

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value)

    return _wrapper


def accepts_right(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in RIGHT state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Right(value):
                return function(value)
            case _:
                return s

    return _wrapper


def accepts_wrong(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in WRONG state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Wrong(value):
                return function(value)
            case _:
                return s

    return _wrapper


def accepts_error(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Error(value):
                return function(value)
            case _:
                return s

    return _wrapper


def accepts_final(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Final(value):
                return function(value)
            case _:
                return s

    return _wrapper


def rejects_right(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in RIGHT state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Right(_):
                return s
            case other:
                return function(other.value)

    return _wrapper


def rejects_wrong(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in WRONG state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Wrong(_):
                return s
            case other:
                return function(other.value)

    return _wrapper


def rejects_error(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in ERROR state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Error(_):
                return s
            case other:
                return function(other.value)

    return _wrapper


def rejects_final(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        match s:
            case Final(_):
                return s
            case other:
                return function(other.value)

    return _wrapper


def switch_to_right(s: State[T]) -> Right[T]:
    """Changes container for Statefull value to Right.

    Args:
        s (State[T]): initial State container

    Returns:
        Right[T]: container
    """
    return Right(s.value)


def switch_to_wrong(s: State[T]) -> Wrong[T]:
    """Changes container for Statefull value to Wrong.

    Args:
        s (State[T]): initial State container

    Returns:
        Wrong[T]: container
    """
    return Wrong(s.value)


def switch_to_error(s: State[T]) -> Error[T]:
    """Changes container for Statefull value to Error.

    Args:
        s (State[T]): initial State container

    Returns:
        Error[T]: container
    """
    return Error(s.value)


def switch_to_final(s: State[T]) -> Right[T]:
    """Changes container for Statefull value to Final.

    Args:
        s (State[T]): initial State container

    Returns:
        Final[T]: container
    """
    return Final(s.value)


Result = Right[T] | Wrong[V]
Safe = Right[T] | Error[TError]
ESafe = Safe[T, Exception]
SafeResult = Right[T] | Wrong[V] | Error[TError]
ESafeResult = SafeResult[T, V, Exception]
