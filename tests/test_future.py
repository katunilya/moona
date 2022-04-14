import inspect
import typing

import pytest

from mona import future


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        1,
        2,
        3,
        object(),
        "some_str",
        b"some_byte_str",
    ],
)
async def test_identity(value: typing.Any):
    value_ = future.identity(value)

    assert inspect.isawaitable(value_)

    value_ = await value_

    assert value_ == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        1,
        2,
        3,
        object(),
        "some_str",
        b"some_byte_str",
    ],
)
async def test_from_value(value: typing.Any):
    future_ = future.from_value(value)

    assert inspect.isawaitable(future_)
    assert isinstance(future_, future.Future)

    future_ = await future_

    assert future_ == value


async def async_plus_1(x: int) -> int:
    return x + 1


async def async_multiply_3(x: int) -> int:
    return x * 3


async def async_strip(x: str) -> str:
    return x.strip()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, function, result",
    [
        (1, lambda x: x, 1),
        ("1", lambda x: x, "1"),
        (3, lambda x: x + 1, 4),
        (3, lambda x: x * 3, 9),
        ("John Doe", lambda s: s.strip(), "John Doe"),
        ("   John Doe  ", lambda s: s.strip(), "John Doe"),
        (1, future.identity, 1),
        ("1", future.identity, "1"),
        (3, async_plus_1, 4),
        (3, async_multiply_3, 9),
        ("John Doe", async_strip, "John Doe"),
        ("   John Doe  ", async_strip, "John Doe"),
    ],
)
async def test_bind(value, function, result):
    future_ = future.from_value(value)

    result_ = future.bind(function, future_)

    assert inspect.isawaitable(result_)
    assert isinstance(result_, future.Future)

    result_ = await result_

    assert result_ == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, functions, result",
    [
        (1, [], 1),
        (1, [future.identity], 1),
        (1, [lambda x: x], 1),
        ("1", [future.identity], "1"),
        ("1", [lambda x: x], "1"),
        (3, [async_plus_1], 4),
        (3, [lambda x: x + 1], 4),
        (3, [async_multiply_3], 9),
        (3, [lambda x: x * 3], 9),
        (1, [lambda x: x + 1, lambda x: x * 3], 6),
        (1, [async_plus_1, async_multiply_3], 6),
        (1, [async_plus_1, lambda x: x * 3], 6),
        (1, [lambda x: x + 1, async_multiply_3], 6),
        ("John Doe", [async_strip], "John Doe"),
        ("   John Doe  ", [async_strip], "John Doe"),
        ("John Doe", [lambda s: s.strip()], "John Doe"),
        ("   John Doe  ", [lambda s: s.strip()], "John Doe"),
    ],
)
async def test_compose(value, functions, result):
    future_ = future.from_value(value)
    composition_ = future.compose(*functions)

    result_ = future_ >> composition_

    assert inspect.isawaitable(result_)
    assert isinstance(result_, future.Future)

    result_ = await result_

    assert result_ == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, functions, result",
    [
        (1, [], 1),
        (1, [future.identity], 1),
        (1, [lambda x: x], 1),
        ("1", [future.identity], "1"),
        ("1", [lambda x: x], "1"),
        (3, [async_plus_1], 4),
        (3, [lambda x: x + 1], 4),
        (3, [async_multiply_3], 9),
        (3, [lambda x: x * 3], 9),
        (1, [lambda x: x + 1, lambda x: x * 3], 6),
        (1, [async_plus_1, async_multiply_3], 6),
        (1, [async_plus_1, lambda x: x * 3], 6),
        (1, [lambda x: x + 1, async_multiply_3], 6),
        ("John Doe", [async_strip], "John Doe"),
        ("   John Doe  ", [async_strip], "John Doe"),
        ("John Doe", [lambda s: s.strip()], "John Doe"),
        ("   John Doe  ", [lambda s: s.strip()], "John Doe"),
    ],
)
async def test_pipe(value, functions, result):
    result_ = future.pipe(
        future.from_value(value),
        *functions,
    )

    assert inspect.isawaitable(result_)
    assert isinstance(result_, future.Future)

    result_ = await result_

    assert result_ == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, function, result",
    [
        (1, lambda x: x, 1),
        ("1", lambda x: x, "1"),
        (3, lambda x: x + 1, 4),
        (3, lambda x: x * 3, 9),
        ("John Doe", lambda s: s.strip(), "John Doe"),
        ("   John Doe  ", lambda s: s.strip(), "John Doe"),
        (1, future.identity, 1),
        ("1", future.identity, "1"),
        (3, async_plus_1, 4),
        (3, async_multiply_3, 9),
        ("John Doe", async_strip, "John Doe"),
        ("   John Doe  ", async_strip, "John Doe"),
    ],
)
async def test_rshift(value, function, result):
    future_ = future.from_value(value)

    result_ = future_ >> function

    assert inspect.isawaitable(result_)
    assert isinstance(result_, future.Future)

    result_ = await result_

    assert result_ == result
