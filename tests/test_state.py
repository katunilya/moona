import pytest

from mona import state2


@pytest.mark.parametrize(
    "arrange_value,act_container_type,assert_value,assert_state,assert_container",
    [
        (1, state2.Right, 1, state2.RIGHT, state2.Right),
        ("1", state2.Right, "1", state2.RIGHT, state2.Right),
        (b"1", state2.Right, b"1", state2.RIGHT, state2.Right),
        ({}, state2.Right, {}, state2.RIGHT, state2.Right),
        (
            {"name": "John Doe"},
            state2.Right,
            {"name": "John Doe"},
            state2.RIGHT,
            state2.Right,
        ),
        (1, state2.Wrong, 1, state2.WRONG, state2.Wrong),
        ("1", state2.Wrong, "1", state2.WRONG, state2.Wrong),
        (b"1", state2.Wrong, b"1", state2.WRONG, state2.Wrong),
        ({}, state2.Wrong, {}, state2.WRONG, state2.Wrong),
        (
            {"name": "John Doe"},
            state2.Wrong,
            {"name": "John Doe"},
            state2.WRONG,
            state2.Wrong,
        ),
        (1, state2.Error, 1, state2.ERROR, state2.Error),
        ("1", state2.Error, "1", state2.ERROR, state2.Error),
        (b"1", state2.Error, b"1", state2.ERROR, state2.Error),
        ({}, state2.Error, {}, state2.ERROR, state2.Error),
        (
            {"name": "John Doe"},
            state2.Error,
            {"name": "John Doe"},
            state2.ERROR,
            state2.Error,
        ),
        (1, state2.Final, 1, state2.FINAL, state2.Final),
        ("1", state2.Final, "1", state2.FINAL, state2.Final),
        (b"1", state2.Final, b"1", state2.FINAL, state2.Final),
        ({}, state2.Final, {}, state2.FINAL, state2.Final),
        (
            {"name": "John Doe"},
            state2.Final,
            {"name": "John Doe"},
            state2.FINAL,
            state2.Final,
        ),
    ],
)
def test_default_containers(
    arrange_value, act_container_type, assert_value, assert_state, assert_container
):
    # arrange
    # act
    s: state2.State = act_container_type(arrange_value)

    # assert
    assert s.value == assert_value
    assert s.__state__ == assert_state
    assert isinstance(s, assert_container)


@pytest.mark.parametrize(
    "arrange_value,act_pack_function,assert_value,assert_state,assert_container",
    [
        (1, state2.right, 1, state2.RIGHT, state2.Right),
        ("1", state2.right, "1", state2.RIGHT, state2.Right),
        (b"1", state2.right, b"1", state2.RIGHT, state2.Right),
        ({}, state2.right, {}, state2.RIGHT, state2.Right),
        (
            {"name": "John Doe"},
            state2.right,
            {"name": "John Doe"},
            state2.RIGHT,
            state2.Right,
        ),
        (1, state2.wrong, 1, state2.WRONG, state2.Wrong),
        ("1", state2.wrong, "1", state2.WRONG, state2.Wrong),
        (b"1", state2.wrong, b"1", state2.WRONG, state2.Wrong),
        ({}, state2.wrong, {}, state2.WRONG, state2.Wrong),
        (
            {"name": "John Doe"},
            state2.wrong,
            {"name": "John Doe"},
            state2.WRONG,
            state2.Wrong,
        ),
        (1, state2.error, 1, state2.ERROR, state2.Error),
        ("1", state2.error, "1", state2.ERROR, state2.Error),
        (b"1", state2.error, b"1", state2.ERROR, state2.Error),
        ({}, state2.error, {}, state2.ERROR, state2.Error),
        (
            {"name": "John Doe"},
            state2.error,
            {"name": "John Doe"},
            state2.ERROR,
            state2.Error,
        ),
        (1, state2.final, 1, state2.FINAL, state2.Final),
        ("1", state2.final, "1", state2.FINAL, state2.Final),
        (b"1", state2.final, b"1", state2.FINAL, state2.Final),
        ({}, state2.final, {}, state2.FINAL, state2.Final),
        (
            {"name": "John Doe"},
            state2.final,
            {"name": "John Doe"},
            state2.FINAL,
            state2.Final,
        ),
    ],
)
def test_pack_functions(
    arrange_value,
    act_pack_function,
    assert_value,
    assert_state,
    assert_container,
):
    # arrange
    # act
    s: state2.State = act_pack_function(arrange_value)

    # assert
    assert s.value == assert_value
    assert s.__state__ == assert_state
    assert isinstance(s, assert_container)


@pytest.mark.parametrize(
    "arrange_s,arrange_function,assert_s",
    [
        (state2.Right(1), lambda x: state2.Right(x + 1), state2.Right(2)),
        (state2.Wrong(1), lambda x: state2.Right(x + 1), state2.Right(2)),
        (state2.Error(1), lambda x: state2.Right(x + 1), state2.Right(2)),
        (state2.Final(1), lambda x: state2.Right(x + 1), state2.Right(2)),
        (state2.Right(1), lambda x: state2.Wrong(x + 1), state2.Wrong(2)),
        (state2.Wrong(1), lambda x: state2.Wrong(x + 1), state2.Wrong(2)),
        (state2.Error(1), lambda x: state2.Wrong(x + 1), state2.Wrong(2)),
        (state2.Final(1), lambda x: state2.Wrong(x + 1), state2.Wrong(2)),
        (state2.Right(1), lambda x: state2.Error(x + 1), state2.Error(2)),
        (state2.Wrong(1), lambda x: state2.Error(x + 1), state2.Error(2)),
        (state2.Error(1), lambda x: state2.Error(x + 1), state2.Error(2)),
        (state2.Final(1), lambda x: state2.Error(x + 1), state2.Error(2)),
        (state2.Right(1), lambda x: state2.Final(x + 1), state2.Final(2)),
        (state2.Wrong(1), lambda x: state2.Final(x + 1), state2.Final(2)),
        (state2.Error(1), lambda x: state2.Final(x + 1), state2.Final(2)),
        (state2.Final(1), lambda x: state2.Final(x + 1), state2.Final(2)),
    ],
)
def test_unpacks(arrange_s, arrange_function, assert_s):
    # arrange
    function = state2.unpacks(arrange_function)

    # act
    s = function(arrange_s)

    # assert
    assert s.value == assert_s.value
    assert s.__state__ == assert_s.__state__


@pytest.mark.parametrize(
    "arrange_s," "arrange_function," "act_guard," "assert_s,",
    [
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_right,
            state2.Right(2),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_wrong,
            state2.Right(1),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_error,
            state2.Right(1),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_final,
            state2.Right(1),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_right,
            state2.Wrong(1),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_wrong,
            state2.Right(2),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_error,
            state2.Wrong(1),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_final,
            state2.Wrong(1),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_right,
            state2.Error(1),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_wrong,
            state2.Error(1),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_error,
            state2.Right(2),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_final,
            state2.Error(1),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_right,
            state2.Final(1),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_wrong,
            state2.Final(1),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_error,
            state2.Final(1),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.accepts_final,
            state2.Right(2),
        ),
        #
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_right,
            state2.Right(1),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_wrong,
            state2.Right(2),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_error,
            state2.Right(2),
        ),
        (
            state2.Right(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_final,
            state2.Right(2),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_right,
            state2.Right(2),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_wrong,
            state2.Wrong(1),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_error,
            state2.Right(2),
        ),
        (
            state2.Wrong(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_final,
            state2.Right(2),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_right,
            state2.Right(2),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_wrong,
            state2.Right(2),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_error,
            state2.Error(1),
        ),
        (
            state2.Error(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_final,
            state2.Right(2),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_right,
            state2.Right(2),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_wrong,
            state2.Right(2),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_error,
            state2.Right(2),
        ),
        (
            state2.Final(1),
            lambda x: state2.Right(x + 1),
            state2.rejects_final,
            state2.Final(1),
        ),
    ],
)
def test_decorators(
    arrange_s,
    arrange_function,
    act_guard,
    assert_s,
):
    # arrange
    function = act_guard(arrange_function)

    # act
    s: state2.State = function(arrange_s)

    # assert
    assert s.value == assert_s.value
    assert s.__state__ == assert_s.__state__
