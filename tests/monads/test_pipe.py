import pytest

from mona.monads.future import Future
from mona.monads.pipe import Pipeline


def test_then():
    assert (
        Pipeline(3)
        .then(lambda x: x + 1)
        .then(lambda x: x**2)
        .then(lambda x: x / 2)
        .then(lambda x: x - 2)
        .then(lambda x: x * 3)
        .finish()
    ) == 18


@pytest.mark.asyncio
async def test_then_future():
    result = await (
        Pipeline(3)
        .then(lambda x: x + 1)
        .then(lambda x: x**2)
        .then_future(Future.identity)
        .then(lambda x: x / 2)
        .then(lambda x: x - 2)
        .then(lambda x: x * 3)
    )
    assert result == 18
