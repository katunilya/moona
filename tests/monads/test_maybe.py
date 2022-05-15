from typing import Callable

import pytest

from moona.monads.maybe import Maybe, Nothing, Some


@pytest.mark.parametrize(
    "cnt, func, result",
    [
        (Some(1), lambda x: x + 1, 2),
        (Some(1), lambda x: Some(x + 1), Some(2)),
        (Some(2), lambda x: x + 1, 3),
        (Some(2), lambda x: Some(x + 1), Some(3)),
        (Some(2), lambda x: Nothing(), Nothing()),
        (Nothing(), lambda x: Some(x + 1), Nothing()),
        (Nothing(), lambda x: x + 1, Nothing()),
    ],
)
def test_bind(cnt: Maybe, func: Callable, result: Maybe):
    assert cnt >> func == result


@pytest.mark.parametrize(
    "cnt, func, result",
    [
        (Some(1), lambda x: x + 1, Some(1)),
        (Some(1), lambda x: Some(x + 1), Some(1)),
        (Some(2), lambda x: x + 1, Some(2)),
        (Some(2), lambda x: Some(x + 1), Some(2)),
        (Some(2), lambda _: Nothing(), Some(2)),
        (Nothing(), lambda _: Some(3), Some(3)),
        (Nothing(), lambda _: 3, 3),
    ],
)
def test_alter(cnt: Maybe, func: Callable, result: Maybe):
    assert cnt << func == result


@pytest.mark.parametrize(
    "cnt, func, result",
    [
        (Some(1), lambda x: x + 1, 2),
        (Some(1), lambda x: Some(x + 1), Some(2)),
        (Nothing(), lambda x: Some(x + 1), Nothing()),
    ],
)
def test_bound(cnt, func, result):
    assert Maybe.if_some(func)(cnt) == result


@pytest.mark.parametrize(
    "cnt, func, result",
    [
        (Some(1), lambda x: x + 1, Some(1)),
        (Some(1), lambda x: Some(x + 1), Some(1)),
        (Nothing(), lambda _: Some(2), Some(2)),
    ],
)
def test_altered(cnt, func, result):
    assert Maybe.if_nothing(func)(cnt) == result


@pytest.mark.parametrize(
    "funcs, cnt, result",
    [
        ([lambda _: Nothing(), lambda x: Some(x)], Some(1), Some(1)),
        ([lambda _: Nothing, lambda x: Some(x)], Nothing(), Nothing()),
        ([lambda _: Nothing()], Nothing(), Nothing()),
        ([lambda _: Nothing()], Some(1), Nothing()),
    ],
)
def test_choose(funcs, cnt, result):
    assert cnt >> Maybe.choose(*funcs) == result


@pytest.mark.parametrize(
    "cnt, func, result",
    [
        (Some(1), lambda x: x if x > 10 else None, Nothing()),
        (Some(11), lambda x: x if x > 10 else None, Some(11)),
    ],
)
def test_no_none(cnt, func, result):
    assert cnt >> Maybe.returns(func) == result


@pytest.mark.parametrize("value", [1, 2, 3, object(), {}, []])
def test_some(value):
    assert Maybe.some(value).value == value


@pytest.mark.parametrize("value", [1, 2, 3, object(), {}, []])
def test_nothing(value):
    assert Maybe.nothing(value) == Nothing()
