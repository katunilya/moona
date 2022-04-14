import dataclasses
import functools
import typing

import toolz

from mona import error as e

T = typing.TypeVar("T")
V = typing.TypeVar("V")
T_ERROR = typing.TypeVar("T_ERROR", bound=BaseException)


@dataclasses.dataclass(frozen=True)
class State(typing.Generic[T]):
    """Container for `State`ful values."""

    value: T
    state: typing.Any


@toolz.curry
def pack(state: typing.Any, value: T) -> State[T]:
    """Curried way of packing value into State container.

    Args:
        state (typing.Any): to assign container
        value (T): to wrap in container

    Returns:
        State[T]: container
    """
    return State(value, state)


def unpack(cnt: State[T]) -> T:
    """Extract value from State container.

    Args:
        cnt (State[T]): container

    Returns:
        T: value
    """
    return cnt.value


def accpets(
    state: typing.Any,
) -> typing.Callable[[typing.Callable[[T], V]], typing.Callable[[State[T]], State[V]]]:
    """Decorator that executes function only if state of container is `state`.

    Args:
        state (typing.Any): target state

    Returns:
        typing.Callable[
            [typing.Callable[[T], V]],
            typing.Callable[[State[T]], State[V]]]: decorator
    """

    def _decorator(
        function: typing.Callable[[T], V]
    ) -> typing.Callable[[State[T]], State[V]]:
        @functools.wraps(function)
        def _wrapper(cnt: State[T]) -> State[V]:
            return function(cnt.value) if cnt.state == state else cnt

        return _wrapper

    return _decorator


def rejects(
    state: typing.Any,
) -> typing.Callable[
    [typing.Callable[[T], State[V]]], typing.Callable[[State[T]], State[V]]
]:
    """Decorator that executes function only if state of container is not `state`.

    Args:
        state (typing.Any): target state

    Returns:
        typing.Callable[
            [typing.Callable[[T], V]],
            typing.Callable[[State[T]], State[V]]]: decorator
    """

    def _decorator(
        function: typing.Callable[[T], State[V]]
    ) -> typing.Callable[[State[T]], State[V]]:
        @functools.wraps(function)
        def _wrapper(cnt: State[T]) -> State[V]:
            return function(cnt.value) if cnt.state != state else cnt

        return _wrapper

    return _decorator


RIGHT = "RIGHT"  # calculation finished successfully
WRONG = "WRONG"  # calculation finished, but result is not appropriate
ERROR = "ERROR"  # calculation finished with error
FINAL = "FINAL"  # calculation is complete and should not be continued


def right(value: T) -> State[T]:
    """Wraps value into State container in RIGHT state.

    Args:
        value (T): to wrap

    Returns:
        State[T]: container
    """
    return State(value, RIGHT)


def wrong(value: T) -> State[T]:
    """Wraps value into State container in WRONG state.

    Args:
        value (T): to wrap

    Returns:
        State[T]: container
    """
    return State(value, WRONG)


def error(value: T) -> State[T]:
    """Wraps value into State container in ERROR state.

    Args:
        value (T): to wrap

    Returns:
        State[T]: container
    """
    return State(value, ERROR)


def final(value: T) -> State[T]:
    """Wraps value into State container in FINAL state.

    Args:
        value (T): to wrap

    Returns:
        State[T]: container
    """
    return State(value, FINAL)


def switch_right(cnt: State[T]) -> State[T]:
    """Changes state of some container to RIGHT.

    Args:
        cnt (State[T]): to switch state

    Returns:
        State[T]: resulting state
    """
    return State(cnt.value, RIGHT)


def switch_wrong(cnt: State[T]) -> State[T]:
    """Changes state of some container to WRONG.

    Args:
        cnt (State[T]): to switch state

    Returns:
        State[T]: resulting state
    """
    return State(cnt.value, WRONG)


def switch_error(cnt: State[T]) -> State[T]:
    """Changes state of some container to ERROR.

    Args:
        cnt (State[T]): to switch state

    Returns:
        State[T]: resulting state
    """
    return State(cnt.value, ERROR)


def switch_final(cnt: State[T]) -> State[T]:
    """Changes state of some container to FINAL.

    Args:
        cnt (State[T]): to switch state

    Returns:
        State[T]: resulting state
    """
    return State(cnt.value, FINAL)


def accepts_right(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on RIGHT state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state == RIGHT else cnt

    return _wrapper


def accepts_wrong(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on WRONG state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state == WRONG else cnt

    return _wrapper


def accepts_error(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on ERROR state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state == ERROR else cnt

    return _wrapper


def accepts_final(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on ERROR state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state == FINAL else cnt

    return _wrapper


def rejects_right(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on not RIGHT state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state != RIGHT else cnt

    return _wrapper


def rejects_wrong(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on not WRONG state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state != WRONG else cnt

    return _wrapper


def rejects_error(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on not ERROR state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state != ERROR else cnt

    return _wrapper


def rejects_final(
    function: typing.Callable[[T], State[V]]
) -> typing.Callable[[State[T]], State[V]]:
    """Function will be executed only on not ERROR state."""

    @functools.wraps(function)
    def _wrapper(cnt: State[T]) -> State[V]:
        return function(cnt.value) if cnt.state != FINAL else cnt

    return _wrapper


RE = typing.Union[State[T], State[e.Error]]
