from typing import Any

import pytest

from mona import state


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.State(5, True)),
        (state.State(5, False), state.State(5, True)),
        (state.State(5, True), state.State(5, True)),
    ],
)
def test_valid(value: Any, monad: state.State[Any]):
    assert state.valid(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.State(5, False)),
        (state.State(5, False), state.State(5, False)),
        (state.State(5, True), state.State(5, False)),
    ],
)
def test_invalid(value: Any, monad: state.State[Any]):
    assert state.invalid(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.State(5, True)),
        (state.State(5, False), state.State(5, False)),
        (state.State(5, True), state.State(5, True)),
    ],
)
def test_pack(value: Any, monad: state.State[Any]):
    assert state.pack(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, 5),
        (state.State(5, False), 5),
        (state.State(5, True), 5),
    ],
)
def test_unpack(value: Any, monad: state.State[Any]):
    assert state.unpack(value) == monad


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.State(2, True)),
        (state.State(1, True), state.State(2, True)),
        (state.State(1, False), state.State(1, False)),
    ],
)
def test_bind(input, output):
    def plus_1(x: int) -> int:
        return x + 1

    assert state.bind(plus_1, input) == output


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.State(2, True)),
        (state.State(1, True), state.State(2, True)),
        (state.State(1, False), state.State(1, False)),
    ],
)
def test_wraps(input, output):
    @state.wrap
    def plus_1(x: int) -> int:
        return x + 1

    assert plus_1(input) == output


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.State(7, True)),
        (state.State(1, True), state.State(7, True)),
        (state.State(1, False), state.State(1, False)),
    ],
)
def test_compose_simple(input, output):

    func = state.compose(
        lambda x: x + 1,
        lambda x: x**2,
        lambda x: x + 3,
    )

    assert func(input) == output


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.State(4, False)),
        (state.State(1, True), state.State(4, False)),
        (state.State(1, False), state.State(1, False)),
        (2, state.State(12, True)),
        (state.State(2, True), state.State(12, True)),
        (state.State(2, False), state.State(2, False)),
    ],
)
def test_compose_with_invalid(input, output):

    func = state.compose(
        lambda x: x + 1,
        lambda x: x**2,
        lambda x: state.valid(x) if x > 5 else state.invalid(x),
        lambda x: x + 3,
    )

    assert func(input) == output


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.State(1, True)),
        (state.State(1, False), state.State(1, False)),
        (4, state.State(5, True)),
        (state.State(4, True), state.State(5, True)),
        (state.State(4, False), state.State(4, False)),
    ],
)
def test_choose(input, output):

    func = state.choose(
        lambda x: state.invalid(x),
        state.compose(
            lambda x: state.valid(x) if x > 3 else state.invalid(x),
            lambda x: x + 1,
        ),
    )

    assert func(input) == output
