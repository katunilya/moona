from typing import Any

import pytest

from mona import state


@pytest.mark.parametrize(
    "monad,valid",
    [
        (5, False),
        (state.Valid(5), True),
        (state.Invalid(5), False),
    ],
)
def test_is_valid(monad: state._State, valid: bool):
    assert state.is_valid(monad) is valid


@pytest.mark.parametrize(
    "monad,valid",
    [
        (5, False),
        (state.Valid(5), False),
        (state.Invalid(5), True),
    ],
)
def test_is_invalid(monad: state._State, valid: bool):
    assert state.is_invalid(monad) is valid


@pytest.mark.parametrize(
    "monad,valid",
    [
        (5, False),
        (state.Valid(5), True),
        (state.Invalid(5), True),
    ],
)
def test_is_state(monad: state._State, valid: bool):
    assert state.is_state(monad) is valid


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.Valid(5)),
        (state.Invalid(5), state.Valid(5)),
        (state.Valid(5), state.Valid(5)),
    ],
)
def test_valid(value: Any, monad: state.State[Any]):
    assert state.valid(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.Invalid(5)),
        (state.Invalid(5), state.Invalid(5)),
        (state.Valid(5), state.Invalid(5)),
    ],
)
def test_invalid(value: Any, monad: state.State[Any]):
    assert state.invalid(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, state.Valid(5)),
        (state.Invalid(5), state.Invalid(5)),
        (state.Valid(5), state.Valid(5)),
    ],
)
def test_pack(value: Any, monad: state.State[Any]):
    assert state.pack(value) == monad


@pytest.mark.parametrize(
    "value,monad",
    [
        (5, 5),
        (state.Invalid(5), 5),
        (state.Valid(5), 5),
    ],
)
def test_unpack(value: Any, monad: state.State[Any]):
    assert state.unpack(value) == monad


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.Valid(2)),
        (state.Valid(1), state.Valid(2)),
        (state.Invalid(1), state.Invalid(1)),
    ],
)
def test_bind(input, output):
    assert state.bind(lambda x: x + 1, input) == output


@pytest.mark.parametrize(
    "input,output",
    [
        (1, state.Valid(7)),
        (state.Valid(1), state.Valid(7)),
        (state.Invalid(1), state.Invalid(1)),
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
        (1, state.Invalid(4)),
        (state.Valid(1), state.Invalid(4)),
        (state.Invalid(1), state.Invalid(1)),
        (2, state.Valid(12)),
        (state.Valid(2), state.Valid(12)),
        (state.Invalid(2), state.Invalid(2)),
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
        (1, state.Valid(1)),
        (state.Invalid(1), state.Invalid(1)),
        (4, state.Valid(5)),
        (state.Valid(4), state.Valid(5)),
        (state.Invalid(4), state.Invalid(4)),
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
    result = func(input)

    assert result == output
