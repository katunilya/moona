import inspect
from typing import Any

import pytest

from mona import future


async def async_identity(x):
    return x


def sync_identity(x):
    return x


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        1,
        2,
        -3,
        {},
        [],
        {"name": "John Doe"},
    ],
)
async def test_pack_value(value: Any):
    _value = future.pack_value(value)
    assert inspect.isawaitable(_value)

    _value = await _value
    assert _value == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, num_of_packings, result",
    [
        (1, 1, 1),
        (1, 2, 1),
        (1, 10, 1),
    ],
)
async def test_pack(value, num_of_packings, result):
    for _ in range(num_of_packings):
        value = future.pack(value)

    assert inspect.isawaitable(value)

    value = await value

    assert value == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value, functions, result",
    [
        (1, [sync_identity], 1),
        (1, [async_identity], 1),
        (1, [async_identity, sync_identity], 1),
        (1, [sync_identity, async_identity], 1),
        (1, [async_identity, async_identity], 1),
        (1, [sync_identity, sync_identity], 1),
        (1, [lambda x: x + 1], 2),
        (1, [lambda x: x + 1, lambda x: x**2], 4),
    ],
)
async def test_bind(value, functions, result):
    for function in functions:
        value = future.bind(function, value)

    assert inspect.isawaitable(value)

    value = await value
    assert value == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value,functions,result",
    [
        (1, [sync_identity], 1),
        (1, [async_identity], 1),
        (1, [sync_identity, async_identity], 1),
        (1, [async_identity, sync_identity], 1),
        (1, [async_identity, async_identity], 1),
        (1, [sync_identity, sync_identity], 1),
        (1, [lambda x: x + 1], 2),
        (1, [lambda x: x + 1, lambda x: x**2], 4),
    ],
)
async def test_compose(value, functions, result):
    composition = future.compose(*functions)

    _value = composition(value)

    assert inspect.isawaitable(_value)

    _value = await _value

    assert _value == result
