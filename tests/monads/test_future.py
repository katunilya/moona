import inspect
from typing import Any

import pytest

from mona.monads.future import Future


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
    result = Future.identity(value)
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
    result = Future.create(value)
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == value


async def async_plus_1(x: int) -> int:
    return x + 1


async def async_multiply_3(x: int) -> int:
    return x * 3


async def async_strip(x: str) -> str:
    return x.strip()


async def identity(x: Any) -> Any:
    return x


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
        (1, identity, 1),
        ("1", identity, "1"),
        (3, async_plus_1, 4),
        (3, async_multiply_3, 9),
        ("John Doe", async_strip, "John Doe"),
        ("   John Doe  ", async_strip, "John Doe"),
    ],
)
async def test_bound(value, func, assert_result):
    result = Future.bound(func)(Future.create(value))
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
        (1, identity, 1),
        ("1", identity, "1"),
        (3, async_plus_1, 4),
        (3, async_multiply_3, 9),
        ("John Doe", async_strip, "John Doe"),
        ("   John Doe  ", async_strip, "John Doe"),
    ],
)
async def test_bind(value, func, assert_result):
    result = Future.create(value) >> func
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == assert_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, func, assert_result",
    [
        (1, [], 1),
        (1, [identity], 1),
        (1, [lambda x: x], 1),
        ("1", [identity], "1"),
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
async def test_compose(value, func, assert_result):
    result = Future.create(value) >> Future.compose(*func)
    assert inspect.isawaitable(result)
    assert isinstance(result, Future)
    assert await result == assert_result
