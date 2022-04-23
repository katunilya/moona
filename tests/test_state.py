import pytest

from mona.monads import state


@pytest.mark.parametrize(
    "arrange_value,act_container_type,assert_value,assert_container",
    [
        (1, state.Right, 1, state.Right),
        ("1", state.Right, "1", state.Right),
        (b"1", state.Right, b"1", state.Right),
        ({}, state.Right, {}, state.Right),
        (
            {"name": "John Doe"},
            state.Right,
            {"name": "John Doe"},
            state.Right,
        ),
        (1, state.Wrong, 1, state.Wrong),
        ("1", state.Wrong, "1", state.Wrong),
        (b"1", state.Wrong, b"1", state.Wrong),
        ({}, state.Wrong, {}, state.Wrong),
        (
            {"name": "John Doe"},
            state.Wrong,
            {"name": "John Doe"},
            state.Wrong,
        ),
        (1, state.Error, 1, state.Error),
        ("1", state.Error, "1", state.Error),
        (b"1", state.Error, b"1", state.Error),
        ({}, state.Error, {}, state.Error),
        (
            {"name": "John Doe"},
            state.Error,
            {"name": "John Doe"},
            state.Error,
        ),
        (1, state.Final, 1, state.Final),
        ("1", state.Final, "1", state.Final),
        (b"1", state.Final, b"1", state.Final),
        ({}, state.Final, {}, state.Final),
        (
            {"name": "John Doe"},
            state.Final,
            {"name": "John Doe"},
            state.Final,
        ),
    ],
)
def test_default_containers(
    arrange_value, act_container_type, assert_value, assert_container
):
    # arrange
    # act
    s: state.State = act_container_type(arrange_value)

    # assert
    assert s.value == assert_value
    assert isinstance(s, assert_container)


@pytest.mark.parametrize(
    "arrange_s,arrange_function,assert_s",
    [
        (state.Right(1), lambda x: state.Right(x + 1), state.Right(2)),
        (state.Wrong(1), lambda x: state.Right(x + 1), state.Right(2)),
        (state.Error(1), lambda x: state.Right(x + 1), state.Right(2)),
        (state.Final(1), lambda x: state.Right(x + 1), state.Right(2)),
        (state.Right(1), lambda x: state.Wrong(x + 1), state.Wrong(2)),
        (state.Wrong(1), lambda x: state.Wrong(x + 1), state.Wrong(2)),
        (state.Error(1), lambda x: state.Wrong(x + 1), state.Wrong(2)),
        (state.Final(1), lambda x: state.Wrong(x + 1), state.Wrong(2)),
        (state.Right(1), lambda x: state.Error(x + 1), state.Error(2)),
        (state.Wrong(1), lambda x: state.Error(x + 1), state.Error(2)),
        (state.Error(1), lambda x: state.Error(x + 1), state.Error(2)),
        (state.Final(1), lambda x: state.Error(x + 1), state.Error(2)),
        (state.Right(1), lambda x: state.Final(x + 1), state.Final(2)),
        (state.Wrong(1), lambda x: state.Final(x + 1), state.Final(2)),
        (state.Error(1), lambda x: state.Final(x + 1), state.Final(2)),
        (state.Final(1), lambda x: state.Final(x + 1), state.Final(2)),
    ],
)
def test_unpacks(arrange_s, arrange_function, assert_s: state.State):
    # arrange
    function = state.unpacks(arrange_function)

    # act
    s = function(arrange_s)

    # assert
    assert s.value == assert_s.value


@pytest.mark.parametrize(
    "arrange_s," "arrange_function," "act_guard," "assert_s,",
    [
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.accepts_right,
            state.Right(2),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.accepts_wrong,
            state.Right(1),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.accepts_error,
            state.Right(1),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.accepts_final,
            state.Right(1),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.accepts_right,
            state.Wrong(1),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.accepts_wrong,
            state.Right(2),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.accepts_error,
            state.Wrong(1),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.accepts_final,
            state.Wrong(1),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.accepts_right,
            state.Error(1),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.accepts_wrong,
            state.Error(1),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.accepts_error,
            state.Right(2),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.accepts_final,
            state.Error(1),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.accepts_right,
            state.Final(1),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.accepts_wrong,
            state.Final(1),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.accepts_error,
            state.Final(1),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.accepts_final,
            state.Right(2),
        ),
        #
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.rejects_right,
            state.Right(1),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.rejects_wrong,
            state.Right(2),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.rejects_error,
            state.Right(2),
        ),
        (
            state.Right(1),
            lambda x: state.Right(x + 1),
            state.rejects_final,
            state.Right(2),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.rejects_right,
            state.Right(2),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.rejects_wrong,
            state.Wrong(1),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.rejects_error,
            state.Right(2),
        ),
        (
            state.Wrong(1),
            lambda x: state.Right(x + 1),
            state.rejects_final,
            state.Right(2),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.rejects_right,
            state.Right(2),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.rejects_wrong,
            state.Right(2),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.rejects_error,
            state.Error(1),
        ),
        (
            state.Error(1),
            lambda x: state.Right(x + 1),
            state.rejects_final,
            state.Right(2),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.rejects_right,
            state.Right(2),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.rejects_wrong,
            state.Right(2),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.rejects_error,
            state.Right(2),
        ),
        (
            state.Final(1),
            lambda x: state.Right(x + 1),
            state.rejects_final,
            state.Final(1),
        ),
    ],
)
def test_decorators(
    arrange_s,
    arrange_function,
    act_guard,
    assert_s: state.State,
):
    # arrange
    function = act_guard(arrange_function)

    # act
    s: state.State = function(arrange_s)

    # assert
    assert s.value == assert_s.value
    assert isinstance(s, type(assert_s))
