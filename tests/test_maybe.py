import pytest

from mona import maybe


def test_nothing_is_singleton():
    assert maybe._Nothing() == maybe.Nothing


@pytest.mark.parametrize(
    "arrange_function,arrange_cnt,assert_cnt",
    [
        (lambda x: maybe.Some(x), maybe.Some(1), maybe.Some(1)),
        (lambda x: maybe.Some(x), maybe.Some(2), maybe.Some(2)),
        (lambda x: maybe.Some(x), maybe.Nothing, maybe.Nothing),
        (lambda x: maybe.Nothing, maybe.Nothing, maybe.Nothing),
        (lambda x: maybe.Nothing, maybe.Some(1), maybe.Nothing),
    ],
)
def test_bind(arrange_function, arrange_cnt, assert_cnt):
    # act
    act_cnt = maybe.bind(arrange_function, arrange_cnt)
    act_cnt_rshift = arrange_cnt >> arrange_function

    # assert
    assert act_cnt == assert_cnt
    assert act_cnt_rshift == assert_cnt


@pytest.mark.parametrize(
    "arrange_recovery_value,arrange_cnt,assert_cnt",
    [
        (1, maybe.Some(1), maybe.Some(1)),
        (2, maybe.Some(1), maybe.Some(1)),
        (2, maybe.Nothing, maybe.Some(2)),
    ],
)
def test_recover(arrange_recovery_value, arrange_cnt, assert_cnt):
    # arrange
    arrange_recover = maybe.recover(arrange_recovery_value)

    # act
    act_cnt = arrange_recover(arrange_cnt)

    # assert
    assert act_cnt == assert_cnt
