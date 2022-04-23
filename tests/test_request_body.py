import dataclasses

import pydantic
import pytest

from mona import context, req
from mona.monads import state


@pytest.mark.parametrize(
    "arrange_body,assert_state,assert_body",
    [
        (b"", state.Right, b""),
        (b"Hello", state.Right, b"Hello"),
        (None, state.Error, req.body.RequestBodyIsNotReceivedError()),
    ],
)
def test_take_body(
    mock_context: context.Context, arrange_body, assert_state, assert_body
):
    # arrange
    mock_context.request.body = arrange_body

    # act
    act_body: state.ESafe[bytes] = req.take_body(mock_context)

    # assert
    assert isinstance(act_body, assert_state)
    assert act_body.value == assert_body


@pytest.mark.parametrize(
    "arrange_body,assert_state,assert_body",
    [
        (b'{"abc": 3}', state.Right, {"abc": 3}),
        (b'{"abc": "some_str"}', state.Right, {"abc": "some_str"}),
        (b"{}", state.Right, {}),  # noqa
        (None, state.Error, req.body.RequestBodyIsNotReceivedError()),
    ],
)
def test_take_body_as_dict(
    mock_context: context.Context, arrange_body, assert_state, assert_body
):
    # arrange
    mock_context.request.body = arrange_body

    # act
    act_body: state.ESafe[dict] = req.take_body_as_dict(mock_context)

    # assert
    assert isinstance(act_body, assert_state)
    assert act_body.value == assert_body


@dataclasses.dataclass
class DataclassUser:  # noqa

    name: str
    age: int


@pytest.mark.parametrize(
    "arrange_body,assert_state,assert_body",
    [
        (
            b'{"name": "Ilya", "age": 21}',
            state.Right,
            DataclassUser(name="Ilya", age=21),
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.Right,
            DataclassUser(name="Marina", age=23),
        ),
        (None, state.Error, req.body.RequestBodyIsNotReceivedError()),
    ],
)
def test_take_body_as_dataclass(
    mock_context: context.Context, arrange_body, assert_state, assert_body
):
    # arrange
    mock_context.request.body = arrange_body
    arrange_handler = req.take_body_as_dataclass(DataclassUser)

    # act
    act_body: state.ESafe[dict] = arrange_handler(mock_context)

    # assert
    assert isinstance(act_body, assert_state)
    assert act_body.value == assert_body


class PydanticUser(pydantic.BaseModel):  # noqa

    name: str
    age: int


@pytest.mark.parametrize(
    "arrange_body,assert_state,assert_body",
    [
        (
            b'{"name": "Ilya", "age": 21}',
            state.Right,
            PydanticUser(name="Ilya", age=21),
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.Right,
            PydanticUser(name="Marina", age=23),
        ),
        (None, state.Error, req.body.RequestBodyIsNotReceivedError()),
    ],
)
def test_take_body_as_pydantic(
    mock_context: context.Context, arrange_body, assert_state, assert_body
):
    mock_context.request.body = arrange_body
    arrange_handler = req.body.take_body_as_pydantic(PydanticUser)

    # act
    act_body: state.ESafe[PydanticUser] = arrange_handler(mock_context)

    # assert
    assert isinstance(act_body, assert_state)
    assert act_body.value == assert_body


@pytest.mark.parametrize(
    "arrange_body,assert_state,assert_body",
    [
        (b"", state.Right, ""),
        (b"Hello", state.Right, "Hello"),
        (
            b'{"name": "Ilya", "age": 21}',
            state.Right,
            """{"name": "Ilya", "age": 21}""",
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.Right,
            """{"name": "Marina", "age": 23}""",
        ),
        (None, state.Error, req.body.RequestBodyIsNotReceivedError()),
    ],
)
def test_take_body_as_str(
    mock_context: context.Context, arrange_body, assert_state, assert_body
):
    # arrange
    mock_context.request.body = arrange_body

    # act
    act_body: state.ESafe[str] = req.take_body_as_str(mock_context)

    # assert
    assert isinstance(act_body, assert_state)
    assert act_body.value == assert_body
