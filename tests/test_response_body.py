import typing

import pydantic
import pytest

from mona import context, error, future, res, state


@pytest.mark.parametrize(
    "arrange_state,arrange_body,assert_state,assert_body",
    [
        (state.RIGHT, b"", state.RIGHT, b""),
        (state.RIGHT, b"Hello, World!", state.RIGHT, b"Hello, World!"),
        (
            state.RIGHT,
            b'{"name": "John Doe", "age": 25}',
            state.RIGHT,
            b'{"name": "John Doe", "age": 25}',
        ),
        (state.WRONG, b"", state.WRONG, b""),
        (state.WRONG, b"Hello, World!", state.WRONG, b"Hello, World!"),
        (
            state.WRONG,
            b'{"name": "John Doe", "age": 25}',
            state.WRONG,
            b'{"name": "John Doe", "age": 25}',
        ),
    ],
)
def test_set_body_bytes(
    mock_context: context.Context,
    arrange_state,
    arrange_body,
    assert_state,
    assert_body,
):
    # arrange
    ctx = state.pack(arrange_state, mock_context)
    handler = res.set_body_bytes(arrange_body)

    # act
    ctx = handler(ctx)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == (
        assert_body if ctx.state == state.RIGHT else None
    )


@pytest.mark.parametrize(
    "arrange_state,arrange_body,assert_state,assert_body",
    [
        (state.RIGHT, "", state.RIGHT, b""),
        (state.RIGHT, "Hello, World!", state.RIGHT, b"Hello, World!"),
        (
            state.RIGHT,
            '{"name": "John Doe", "age": 25}',
            state.RIGHT,
            b'{"name": "John Doe", "age": 25}',
        ),
        (state.WRONG, "", state.WRONG, b""),
        (state.WRONG, "Hello, World!", state.WRONG, b"Hello, World!"),
        (
            state.WRONG,
            '{"name": "John Doe", "age": 25}',
            state.WRONG,
            b'{"name": "John Doe", "age": 25}',
        ),
    ],
)
def test_set_body_text(
    mock_context: context.Context,
    arrange_state,
    arrange_body,
    assert_state,
    assert_body,
):
    # arrange
    ctx = state.pack(arrange_state, mock_context)
    handler = res.set_body_text(arrange_body)

    # act
    ctx = handler(ctx)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == (
        assert_body if ctx.state == state.RIGHT else None
    )


# Functions for test-cases of `set_body_from_bytes`


def sync_set_right_concrete_bytes(bts: typing.ByteString):  # noqa
    return lambda ctx: state.right(bts)


def sync_set_error_concrete_bytes(ctx):  # noqa
    return state.error(error.Error("sync_set_error_concrete_bytes Error occurred."))


def async_set_right_concrete_bytes(bts: typing.ByteString):  # noqa
    async def _setter(ctx):
        return state.right(bts)

    return _setter


async def async_set_error_concrete_bytes(ctx):  # noqa
    return state.error(error.Error("async_set_error_concrete_bytes Error occurred."))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.RIGHT, sync_set_right_concrete_bytes(b""), state.RIGHT, b""),
        (state.RIGHT, sync_set_right_concrete_bytes(b"ABCD"), state.RIGHT, b"ABCD"),
        (
            state.RIGHT,
            sync_set_right_concrete_bytes(b'{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (state.WRONG, sync_set_right_concrete_bytes(b""), state.WRONG, None),
        (state.WRONG, sync_set_right_concrete_bytes(b"ABCD"), state.WRONG, None),
        (
            state.WRONG,
            sync_set_right_concrete_bytes(b'{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (state.RIGHT, async_set_right_concrete_bytes(b""), state.RIGHT, b""),
        (state.RIGHT, async_set_right_concrete_bytes(b"ABCD"), state.RIGHT, b"ABCD"),
        (
            state.RIGHT,
            async_set_right_concrete_bytes(b'{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (state.WRONG, async_set_right_concrete_bytes(b""), state.WRONG, None),
        (state.WRONG, async_set_right_concrete_bytes(b"ABCD"), state.WRONG, None),
        (
            state.WRONG,
            async_set_right_concrete_bytes(b'{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (
            state.RIGHT,
            sync_set_error_concrete_bytes,
            state.ERROR,
            b"sync_set_error_concrete_bytes Error occurred.",
        ),
        (
            state.RIGHT,
            async_set_error_concrete_bytes,
            state.ERROR,
            b"async_set_error_concrete_bytes Error occurred.",
        ),
        (state.WRONG, sync_set_error_concrete_bytes, state.WRONG, None),
        (state.WRONG, async_set_error_concrete_bytes, state.WRONG, None),
    ],
)
async def test_set_body_from_bytes(
    mock_context: context.Context,
    arrange_state,
    act_function,
    assert_state,
    assert_body,
):
    # arrange
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_body_from_bytes(act_function)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == assert_body


# Functions for test-cases of `set_body_from_dict`


def sync_set_right_concrete_dict(dct: dict):  # noqa
    return lambda ctx: state.right(dct)


def sync_set_error_concrete_dict(ctx):  # noqa
    return state.error(error.Error("sync_set_error_concrete_dict Error occurred."))


def async_set_right_concrete_dict(dct: dict):  # noqa
    async def _setter(ctx):
        return state.right(dct)

    return _setter


async def async_set_error_concrete_dict(ctx):  # noqa
    return state.error(error.Error("async_set_error_concrete_dict Error occurred."))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.RIGHT, sync_set_right_concrete_dict({}), state.RIGHT, b"{}"),  # noqa
        (
            state.RIGHT,
            sync_set_right_concrete_dict({"name": "John Doe"}),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_dict(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (
            state.RIGHT,
            sync_set_error_concrete_dict,
            state.ERROR,
            b"sync_set_error_concrete_dict Error occurred.",
        ),
        (state.RIGHT, async_set_right_concrete_dict({}), state.RIGHT, b"{}"),  # noqa
        (
            state.RIGHT,
            async_set_right_concrete_dict({"name": "John Doe"}),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            async_set_right_concrete_dict(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (
            state.RIGHT,
            async_set_error_concrete_dict,
            state.ERROR,
            b"async_set_error_concrete_dict Error occurred.",
        ),
        (state.WRONG, sync_set_right_concrete_dict({}), state.WRONG, None),  # noqa
        (
            state.WRONG,
            sync_set_right_concrete_dict({"name": "John Doe"}),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_dict(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, sync_set_error_concrete_dict, state.WRONG, None),
        (state.WRONG, async_set_right_concrete_dict({}), state.WRONG, None),  # noqa
        (
            state.WRONG,
            async_set_right_concrete_dict({"name": "John Doe"}),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            async_set_right_concrete_dict(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, async_set_error_concrete_dict, state.WRONG, None),
    ],
)
async def test_set_body_from_dict(
    mock_context: context.Context,
    arrange_state,
    act_function,
    assert_state,
    assert_body,
):
    # arrange
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_body_from_dict(act_function)

    # act
    ctx: context.StateContext = await (ctx >> handler)
    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == assert_body


# Functions and classes for test-cases of `set_body_from_dict`


class User(pydantic.BaseModel):  # noqa
    name: str


class UserInfo(pydantic.BaseModel):  # noqa
    age: int
    city: str


class ExtendedUser(pydantic.BaseModel):  # noqa
    name: str
    info: UserInfo


def sync_set_right_concrete_pydantic_model(model: pydantic.BaseModel):  # noqa
    return lambda ctx: state.right(model)


def sync_set_error_concrete_pydantic_model(ctx):  # noqa
    return state.error(
        error.Error("sync_set_error_concrete_pydantic_model Error occurred.")
    )


def async_set_right_concrete_pydantic_model(model: pydantic.BaseModel):  # noqa
    async def _setter(ctx):
        return state.right(model)

    return _setter


async def async_set_error_concrete_pydantic_model(ctx):  # noqa
    return state.error(
        error.Error("async_set_error_concrete_pydantic_model Error occurred.")
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (
            state.RIGHT,
            sync_set_right_concrete_pydantic_model(pydantic.BaseModel()),
            state.RIGHT,
            b"{}",  # noqa
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_pydantic_model(User(name="John Doe")),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_pydantic_model(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (
            state.RIGHT,
            sync_set_error_concrete_pydantic_model,
            state.ERROR,
            b"sync_set_error_concrete_pydantic_model Error occurred.",
        ),
        (
            state.RIGHT,
            async_set_right_concrete_pydantic_model(pydantic.BaseModel()),
            state.RIGHT,
            b"{}",  # noqa
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_pydantic_model(User(name="John Doe")),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            async_set_right_concrete_pydantic_model(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (
            state.RIGHT,
            async_set_error_concrete_pydantic_model,
            state.ERROR,
            b"async_set_error_concrete_pydantic_model Error occurred.",
        ),
        #
        (
            state.WRONG,
            sync_set_right_concrete_pydantic_model(pydantic.BaseModel()),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_pydantic_model(User(name="John Doe")),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_pydantic_model(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, sync_set_error_concrete_pydantic_model, state.WRONG, None),
        (
            state.WRONG,
            async_set_right_concrete_pydantic_model(pydantic.BaseModel()),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_pydantic_model(User(name="John Doe")),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            async_set_right_concrete_pydantic_model(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, async_set_error_concrete_pydantic_model, state.WRONG, None),
    ],
)
async def test_set_body_from_pydantic(
    mock_context: context.Context,
    arrange_state,
    act_function,
    assert_state,
    assert_body,
):
    # arrange
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_body_from_pydantic(act_function)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == assert_body
