import inspect

import pytest

from moona.monads.future import Future


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
async def test_identity(value):
    result = Future.this(value)
    assert inspect.isawaitable(result)
    assert not isinstance(result, Future)
    assert await result == value


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
async def test_create(value):
    result = Future.from_value(value)
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == value


async def async_plus_1(x: int) -> int:
    return x + 1


async def async_multiply_3(x: int) -> int:
    return x * 3


async def async_strip(x: str) -> str:
    return x.strip()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (1, Future.this, 1),
        ("1", Future.this, "1"),
        (3, async_plus_1, 4),
        (3, async_multiply_3, 9),
        ("John Doe", async_strip, "John Doe"),
        ("   John Doe  ", async_strip, "John Doe"),
    ],
)
async def test_bind_async(value, func, assert_result):
    result = Future.from_value(value) >> func
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == assert_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (1, lambda x: x, 1),
        ("1", lambda x: x, "1"),
        (3, lambda x: x + 1, 4),
        (3, lambda x: x * 3, 9),
        ("John Doe", lambda s: s.strip(), "John Doe"),
        ("   John Doe  ", lambda s: s.strip(), "John Doe"),
    ],
)
async def test_bind_sync(value, func, assert_result):
    result = Future.from_value(value) > func
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == assert_result
