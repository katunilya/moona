import inspect

import pytest

from mona.monads import future


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_value",
    [
        1,
        2,
        3,
        object(),
        "some_str",
        b"some_byte_str",
    ],
)
async def test_identity(arrange_value):
    # act
    act_value = future.identity(arrange_value)

    # assert
    assert inspect.isawaitable(act_value)

    # act
    act_value = await act_value

    # assert
    assert act_value == arrange_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_value",
    [
        1,
        2,
        3,
        object(),
        "some_str",
        b"some_byte_str",
    ],
)
async def test_from_value(arrange_value):
    # act
    act_value = future.from_value(arrange_value)

    # assert
    assert inspect.isawaitable(act_value)
    assert isinstance(act_value, future.Future)

    # act
    act_value = await act_value

    # assert
    assert act_value == arrange_value


async def async_plus_1(x: int) -> int:
    return x + 1


async def async_multiply_3(x: int) -> int:
    return x * 3


async def async_strip(x: str) -> str:
    return x.strip()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_value, arrange_function, assert_value",
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
async def test_bind(arrange_value, arrange_function, assert_value):
    # arrange
    arrange_future = future.from_value(arrange_value)

    # act
    act_value = future.bind(arrange_function, arrange_future)

    # assert
    assert inspect.isawaitable(act_value)
    assert isinstance(act_value, future.Future)

    # act
    act_value = await act_value

    # assert
    assert act_value == assert_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_value, arrange_functions, assert_value",
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
async def test_compose(arrange_value, arrange_functions, assert_value):
    # assert
    arrange_future = future.from_value(arrange_value)
    arrange_composition = future.compose(*arrange_functions)

    # act
    act_value = arrange_future >> arrange_composition

    # assert
    assert inspect.isawaitable(act_value)
    assert isinstance(act_value, future.Future)

    # act
    act_value = await act_value

    # assert
    assert act_value == assert_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_value, arrange_functions, assert_value",
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
async def test_pipe(arrange_value, arrange_functions, assert_value):
    # act
    act_value = future.pipe(
        future.from_value(arrange_value),
        *arrange_functions,
    )

    # assert
    assert inspect.isawaitable(act_value)
    assert isinstance(act_value, future.Future)

    # act
    act_value = await act_value

    # assert
    assert act_value == assert_value


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
