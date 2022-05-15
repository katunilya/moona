import pytest

from moona.monads.result import Error, Ok, Result


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
    result = Result.ok(value)
    assert isinstance(result, Result)
    assert isinstance(result, Ok)
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
    result = Result.bad(value)
    assert isinstance(result, Result)
    assert isinstance(result, Error)
    assert result.value == value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: Ok(x + 1), Ok(2)),
        (Ok(1), lambda x: Error(x + 1), Error(2)),
        (Error(1), lambda x: Ok(x + 1), Ok(1)),
        (Error(1), lambda x: Error(x + 1), Ok(1)),
    ],
)
def test_bound(value, func, assert_result: Result):
    result = Result.if_ok(func)(value)
    assert result.value == assert_result.value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: Ok(x + 1), Ok(1)),
        (Ok(1), lambda x: Error(x + 1), Ok(1)),
        (Error(1), lambda x: Ok(x + 1), Ok(2)),
        (Error(1), lambda x: Error(x + 1), Error(2)),
    ],
)
def test_altered(value, func, assert_result: Result):
    result = Result.if_error(func)(value)
    assert result.value == assert_result.value


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: x + 1, 2),
        (Error(1), lambda x: x + 1, Error(1)),
        (Ok(1), lambda x: Ok(x + 1), Ok(2)),
        (Error(1), lambda x: Ok(x + 1), Error(1)),
    ],
)
def test_bind(value, func, assert_result):
    assert value >> func == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: x + 1, Ok(1)),
        (Error(1), lambda x: x + 1, 2),
        (Ok(1), lambda x: Ok(x + 1), Ok(1)),
        (Error(1), lambda x: Ok(x + 1), Ok(2)),
    ],
)
def test_alter(value, func, assert_result):
    assert value << func == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: 10 // x, Ok(10)),
        (Ok(2), lambda x: 10 // x, Ok(5)),
        (Ok(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safe(value, func, assert_result):
    result = value >> Result.returns(func)

    match result:
        case Error(value=Exception() as err):
            assert isinstance(err, assert_result)
        case Ok() as value:
            assert value == assert_result


@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (Ok(1), lambda x: 10 // x, Ok(10)),
        (Ok(2), lambda x: 10 // x, Ok(5)),
        (Ok(0), lambda x: 10 // x, ZeroDivisionError),
    ],
)
def test_safely_bound(value, func, assert_result):
    result = Result.if_ok_safe(func)(value)

    match result:
        case Error(value=Exception() as err):
            assert isinstance(err, assert_result)
        case Ok() as value:
            assert value == assert_result
