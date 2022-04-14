from dataclasses import dataclass
from typing import ByteString

import pytest
from pydantic import BaseModel

from mona import req, state
from mona.context import Context
from mona.req.body import RequestBodyIsNotReceivedError


@pytest.mark.parametrize(
    "raw_body,target_state,target_value,error_type",
    [
        (b"", state.RIGHT, b"", None),
        (b"Hello", state.RIGHT, b"Hello", None),
        (None, state.ERROR, None, RequestBodyIsNotReceivedError),
    ],
)
def test_take_body(
    mock_context: Context, raw_body, target_state, target_value, error_type
):
    mock_context.request.body = raw_body

    body: state.RE[ByteString] = req.take_body(mock_context)

    assert body.state == target_state

    if body.state == state.ERROR:
        assert isinstance(body.value, error_type)
    else:
        assert body.value == target_value


@pytest.mark.parametrize(
    "raw_body,target_state,target_value,error_type",
    [
        (b'{"abc": 3}', state.RIGHT, {"abc": 3}, None),
        (b'{"abc": "some_str"}', state.RIGHT, {"abc": "some_str"}, None),
        (b"{}", state.RIGHT, {}, None),  # noqa
        (None, state.ERROR, None, RequestBodyIsNotReceivedError),
    ],
)
def test_take_body_as_dict(
    mock_context: Context, raw_body, target_state, target_value, error_type
):
    mock_context.request.body = raw_body

    body: state.RE[dict] = req.take_body_as_dict(mock_context)

    assert body.state == target_state

    if body.state == state.ERROR:
        assert isinstance(body.value, error_type)
    else:
        assert body.value == target_value


@dataclass
class DataclassUser:  # noqa

    name: str
    age: int


@pytest.mark.parametrize(
    "raw_body,target_state,target_value,error_type",
    [
        (
            b'{"name": "Ilya", "age": 21}',
            state.RIGHT,
            DataclassUser(name="Ilya", age=21),
            None,
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.RIGHT,
            DataclassUser(name="Marina", age=23),
            None,
        ),
        (None, state.ERROR, None, RequestBodyIsNotReceivedError),
    ],
)
def test_take_body_as_dataclass(
    mock_context: Context, raw_body, target_state, target_value, error_type
):
    mock_context.request.body = raw_body
    _handler = req.take_body_as_dataclass(DataclassUser)

    body: state.RE[dict] = _handler(mock_context)

    assert body.state == target_state

    if body.state == state.ERROR:
        assert isinstance(body.value, error_type)
    else:
        assert body.value == target_value


class PydanticUser(BaseModel):  # noqa

    name: str
    age: int


@pytest.mark.parametrize(
    "raw_body,target_state,target_value,error_type",
    [
        (
            b'{"name": "Ilya", "age": 21}',
            state.RIGHT,
            PydanticUser(name="Ilya", age=21),
            None,
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.RIGHT,
            PydanticUser(name="Marina", age=23),
            None,
        ),
        (None, state.ERROR, None, RequestBodyIsNotReceivedError),
    ],
)
def test_take_body_as_pydantic(
    mock_context: Context, raw_body, target_state, target_value, error_type
):
    mock_context.request.body = raw_body
    _handler = req.take_body_as_pydantic(PydanticUser)

    body: state.RE[dict] = _handler(mock_context)

    assert body.state == target_state

    if body.state == state.ERROR:
        assert isinstance(body.value, error_type)
    else:
        assert body.value == target_value


@pytest.mark.parametrize(
    "raw_body,target_state,target_value,error_type",
    [
        (b"", state.RIGHT, "", None),
        (b"Hello", state.RIGHT, "Hello", None),
        (
            b'{"name": "Ilya", "age": 21}',
            state.RIGHT,
            """{"name": "Ilya", "age": 21}""",
            None,
        ),
        (
            b'{"name": "Marina", "age": 23}',
            state.RIGHT,
            """{"name": "Marina", "age": 23}""",
            None,
        ),
        (None, state.ERROR, None, RequestBodyIsNotReceivedError),
    ],
)
def test_take_body_as_str(
    mock_context: Context, raw_body, target_state, target_value, error_type
):
    mock_context.request.body = raw_body

    body: state.RE[ByteString] = req.take_body_as_str(mock_context)

    assert body.state == target_state

    if body.state == state.ERROR:
        assert isinstance(body.value, error_type)
    else:
        assert body.value == target_value
