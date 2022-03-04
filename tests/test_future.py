import inspect

import pytest

from mona import future

# TODO improve structure of tests for Future monad (decompose)


async def async_identity(x):
    return x


def sync_identity(x):
    return x


@pytest.mark.asyncio
async def test_pack():

    result = future.pack(3)
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3

    result = future.pack(future.pack(3))
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3


@pytest.mark.asyncio
async def test_bind():

    result = future.bind(async_identity, 3)
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3

    result = future.bind(sync_identity, 3)
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3

    result = future.bind(async_identity, 3)
    result = future.bind(sync_identity, result)
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3

    result = future.bind(async_identity, 3)
    result = future.bind(async_identity, result)
    assert inspect.isawaitable(result)

    result = await result
    assert result == 3


def plus(x, y):
    return x + y


def plus_1(x):
    return plus(1, x)


@pytest.mark.asyncio
async def test_compose():
    func = future.compose(
        sync_identity,
        plus_1,
    )

    result = func(1)
    assert inspect.isawaitable(result)
    result = await result
    assert result == 2


@future.wrap
def sync_function(x: int) -> int:
    return (x + 1) ** 2


@pytest.mark.asyncio
async def test_wrap():

    result = sync_function(3)
    assert inspect.isawaitable(result)
    result = await result
    assert result == 16

    result = sync_function(future.pack(3))
    assert inspect.isawaitable(result)
    result = await result
    assert result == 16

    f = future.wrap(future.pack)
    result = f(1)
    assert inspect.isawaitable(result)
    result = await result
    assert result == 1
