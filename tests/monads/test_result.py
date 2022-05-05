import pytest

from mona.monads.result import Failure, Result, Success


@pytest.mark.parametrize(
    "value",
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
def test_successfull(value):
    result = Result.successfull(value)
    assert isinstance(result, Result)
    assert isinstance(result, Success)
    assert result.value == value


@pytest.mark.parametrize(
    "value",
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
def test_failed(value):
    result = Result.failed(value)
    assert isinstance(result, Result)
    assert isinstance(result, Failure)
    assert result.value == value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: Success(x + 1), Success(2)),
        (Success(1), lambda x: Failure(x + 1), Failure(2)),
        (Failure(1), lambda x: Success(x + 1), Success(1)),
        (Failure(1), lambda x: Failure(x + 1), Success(1)),
    ],
)
def test_bound(value, func, assert_result: Result):
    result = Result.bound(func)(value)
    assert result.value == assert_result.value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: Success(x + 1), Success(1)),
        (Success(1), lambda x: Failure(x + 1), Success(1)),
        (Failure(1), lambda x: Success(x + 1), Success(2)),
        (Failure(1), lambda x: Failure(x + 1), Failure(2)),
    ],
)
def test_altered(value, func, assert_result: Result):
    result = Result.altered(func)(value)
    assert result.value == assert_result.value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: x + 1, 2),
        (Failure(1), lambda x: x + 1, Failure(1)),
        (Success(1), lambda x: Success(x + 1), Success(2)),
        (Failure(1), lambda x: Success(x + 1), Failure(1)),
    ],
)
def test_bind(value, func, assert_result):
    assert value >> func == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: x + 1, Success(1)),
        (Failure(1), lambda x: x + 1, 2),
        (Success(1), lambda x: Success(x + 1), Success(1)),
        (Failure(1), lambda x: Success(x + 1), Success(2)),
    ],
)
def test_alter(value, func, assert_result):
    assert value << func == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: 10 // x, Success(10)),
        (Success(2), lambda x: 10 // x, Success(5)),
        (Success(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safe(value, func, assert_result):
    result = value >> Result.safe(func)

    match result:
        case Failure(value=Exception() as err):
            assert isinstance(err, assert_result)
        case Success() as value:
            assert value == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Success(1), lambda x: 10 // x, Success(10)),
        (Success(2), lambda x: 10 // x, Success(5)),
        (Success(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safely_bound(value, func, assert_result):
    result = Result.safely_bound(func)(value)

    match result:
        case Failure(value=Exception() as err):
            assert isinstance(err, assert_result)
        case Success() as value:
            assert value == assert_result
