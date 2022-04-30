import pytest

from mona.monads.result import Failure, Result, Success


@pytest.mark.parametrize(
    "arrange_value",
    [
        1,
        2,
        3,
        {},
        object(),
        b"test",
        "test",
    ],
)
def test_successfull(arrange_value):
    # act
    act_value = Result.successfull(arrange_value)

    # assert
    assert isinstance(act_value, Result)
    assert isinstance(act_value, Success)
    assert act_value.value == arrange_value


@pytest.mark.parametrize(
    "arrange_value",
    [
        1,
        2,
        3,
        {},
        object(),
        b"test",
        "test",
    ],
)
def test_failed(arrange_value):
    # act
    act_value = Result.failed(arrange_value)

    # assert
    assert isinstance(act_value, Result)
    assert isinstance(act_value, Failure)
    assert act_value.value == arrange_value


@pytest.mark.parametrize(
    "arrange_s,arrange_function,assert_s",
    [
        (Success(1), lambda x: Success(x + 1), Success(2)),
        (Success(1), lambda x: Failure(x + 1), Failure(2)),
        (Failure(1), lambda x: Success(x + 1), Success(1)),
        (Failure(1), lambda x: Failure(x + 1), Success(1)),
    ],
)
def test_bound(arrange_s, arrange_function, assert_s: Result):
    # arrange
    function = Result.bound(arrange_function)

    # act
    s = function(arrange_s)

    # assert
    assert s.value == assert_s.value


@pytest.mark.parametrize(
    "arrange_s,arrange_function,assert_s",
    [
        (Success(1), lambda x: Success(x + 1), Success(1)),
        (Success(1), lambda x: Failure(x + 1), Success(1)),
        (Failure(1), lambda x: Success(x + 1), Success(2)),
        (Failure(1), lambda x: Failure(x + 1), Failure(2)),
    ],
)
def test_altered(arrange_s, arrange_function, assert_s: Result):
    # arrange
    function = Result.altered(arrange_function)

    # act
    s = function(arrange_s)

    # assert
    assert s.value == assert_s.value


@pytest.mark.parametrize(
    "arrange_value, arrange_func, assert_value",
    [
        (Success(1), lambda x: x + 1, 2),
        (Failure(1), lambda x: x + 1, Failure(1)),
        (Success(1), lambda x: Success(x + 1), Success(2)),
        (Failure(1), lambda x: Success(x + 1), Failure(1)),
    ],
)
def test_bind(arrange_value, arrange_func, assert_value):
    # act
    act_value = arrange_value >> arrange_func

    # assert
    assert act_value == assert_value


@pytest.mark.parametrize(
    "arrange_value, arrange_func, assert_value",
    [
        (Success(1), lambda x: x + 1, Success(1)),
        (Failure(1), lambda x: x + 1, 2),
        (Success(1), lambda x: Success(x + 1), Success(1)),
        (Failure(1), lambda x: Success(x + 1), Success(2)),
    ],
)
def test_alter(arrange_value, arrange_func, assert_value):
    # act
    act_value = arrange_value << arrange_func

    # assert
    assert act_value == assert_value


@pytest.mark.parametrize(
    "arrange_value, arrange_func, assert_value",
    [
        (Success(1), lambda x: 10 // x, Success(10)),
        (Success(2), lambda x: 10 // x, Success(5)),
        (Success(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safe(arrange_value, arrange_func, assert_value):
    # act
    act_value = arrange_value >> Result.safe(arrange_func)

    # assert
    match act_value:
        case Failure(value=Exception() as err):
            assert isinstance(err, assert_value)
        case Success() as value:
            assert value == assert_value


@pytest.mark.parametrize(
    "arrange_value, arrange_func, assert_value",
    [
        (Success(1), lambda x: 10 // x, Success(10)),
        (Success(2), lambda x: 10 // x, Success(5)),
        (Success(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safely_bound(arrange_value, arrange_func, assert_value):
    # act
    act_value = Result.safely_bound(arrange_func)(arrange_value)

    # assert
    match act_value:
        case Failure(value=Exception() as err):
            assert isinstance(err, assert_value)
        case Success() as value:
            assert value == assert_value
