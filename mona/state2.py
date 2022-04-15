import abc
import functools
import typing

T = typing.TypeVar("T")
V = typing.TypeVar("V")
TError = typing.TypeVar("TError", bound=Exception)


class State(abc.ABC, typing.Generic[T]):
    """Base container for Statefull values."""

    __slots__ = "value", "__state__"
    __state__: str
    value: T

    def __init__(self, value: T) -> None:
        """Base container for Statefull values.

        Args:
            value (T): to have state
        """
        super().__init__()
        self.value = value


RIGHT = "RIGHT"  # value should be processed next
WRONG = "WRONG"  # value should not be processed next
ERROR = "ERROR"  # value should not be processed next due to error
FINAL = "FINAL"  # value should not be processed next as processing finished


class Right(State[T]):
    """Value should be processed next."""

    __state__ = RIGHT


class Wrong(State[T]):
    """Value should not be processed next."""

    __state__ = WRONG


class Error(State[TError]):
    """Value should not be processed next due to error."""

    __state__ = ERROR


class Final(State[T]):
    """Value should not be processed next as processing finished."""

    __state__ = FINAL


def right(value: T) -> Right[T]:
    """Packs value into RIGHT state.

    Args:
        value (T): to pack into RIGHT state

    Returns:
        Right[T]: packed value
    """
    return Right(value)


def wrong(value: T) -> Right[T]:
    """Packs value into WRONG state.

    Args:
        value (T): to pack into WRONG state

    Returns:
        Wrong[T]: packed value
    """
    return Wrong(value)


def error(value: TError) -> Error[TError]:
    """Packs value into ERROR state.

    Args:
        value (TError): to pack into ERROR state

    Returns:
        Error[TError]: packed value
    """
    return Error(value)


def final(value: T) -> Final[T]:
    """Packs value into FINAL state.

    Args:
        value (T): to pack into FINAL state

    Returns:
        Final[T]: packed value
    """
    return Final(value)


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
        return function(s.value) if s.__state__ == RIGHT else s

    return _wrapper


def accepts_wrong(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in WRONG state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ == WRONG else s

    return _wrapper


def accepts_error(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ == ERROR else s

    return _wrapper


def accepts_final(function: typing.Callable[[T], State[V]]):
    """Decorator that executes guarded function only when monad is in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ == FINAL else s

    return _wrapper


def rejects_right(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in RIGHT state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ != RIGHT else s

    return _wrapper


def rejects_wrong(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in WRONG state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ != WRONG else s

    return _wrapper


def rejects_error(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in ERROR state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ != ERROR else s

    return _wrapper


def rejects_final(function: typing.Callable[[T], State[V]]):
    """Decorator that guards function from container in FINAL state.

    This decorator also unpacks `State` container.
    """

    @functools.wraps(function)
    def _wrapper(s: State[T]):
        return function(s.value) if s.__state__ != FINAL else s

    return _wrapper
