"""Tests for `State` monad."""
import pytest

from mona import state


@pytest.mark.parametrize(
    "value, init_state, target_state",
    [
        (1, 1, 2),
        ("1", 1, 2),
        (object(), 1, 2),
        (1, "1", "2"),
        ("1", "1", "2"),
        (object(), "1", "2"),
        (1, object(), object()),
        ("1", object(), object()),
        (object(), object(), object()),
    ],
)
def test_pack(value, init_state, target_state):
    cnt: state.State = state.pack(target_state, value)

    assert cnt.state == target_state
    assert cnt.value == value


@pytest.mark.parametrize(
    "value, init_state, target_state",
    [
        (1, 1, 2),
        ("1", 1, 2),
        (object(), 1, 2),
        (1, "1", "2"),
        ("1", "1", "2"),
        (object(), "1", "2"),
        (1, object(), object()),
        ("1", object(), object()),
        (object(), object(), object()),
    ],
)
def test_curry_pack(value, init_state, target_state):
    switcher = state.pack(target_state)

    cnt: state.State = switcher(value)

    assert cnt.state == target_state
    assert cnt.value == value


@pytest.mark.parametrize(
    "value, init_state, guard_state, target_value, target_state, function",
    [
        (1, 1, 1, 1, 1, lambda x: state.State(x, 1)),
        (1, 1, 2, 1, 1, lambda x: state.State(x + 1, 1)),
        (1, 1, 2, 1, 1, lambda x: state.State(x + 1, 3)),
        (1, 1, 1, 2, 3, lambda x: state.State(x + 1, 3)),
    ],
)
def test_accepts(value, init_state, guard_state, target_value, target_state, function):
    cnt = state.State(value, init_state)
    guard = state.accpets(guard_state)
    function = guard(function)

    cnt = function(cnt)

    assert cnt.value == target_value
    assert cnt.state == target_state


@pytest.mark.parametrize(
    "value, init_state, guard_state, target_value, target_state, function",
    [
        (1, 1, 2, 1, 1, lambda x: state.State(x, 1)),
        (1, 1, 1, 1, 1, lambda x: state.State(x + 1, 1)),
        (1, 1, 1, 1, 1, lambda x: state.State(x + 1, 3)),
        (1, 1, 2, 2, 3, lambda x: state.State(x + 1, 3)),
    ],
)
def test_rejects(value, init_state, guard_state, target_value, target_state, function):
    cnt = state.State(value, init_state)
    guard = state.rejects(guard_state)
    function = guard(function)

    cnt = function(cnt)

    assert cnt.value == target_value
    assert cnt.state == target_state


@pytest.mark.parametrize(
    "switcher, target_state",
    [
        (state.right, state.RIGHT),
        (state.wrong, state.WRONG),
        (state.error, state.ERROR),
        (state.final, state.FINAL),
    ],
)
def test_state_switching(
    switcher,
    target_state,
):
    ctx: state.State[int] = switcher(1)

    assert ctx.state == target_state
