import pydantic
import pytest

from mona import context, future, res, state


@pytest.mark.parametrize(
    "arrange_state,arrange_body,assert_state,assert_body",
    [
        (state.Right, b"", state.Right, b""),
        (state.Right, b"Hello, World!", state.Right, b"Hello, World!"),
        (
            state.Right,
            b'{"name": "John Doe", "age": 25}',
            state.Right,
            b'{"name": "John Doe", "age": 25}',
        ),
        (state.Wrong, b"", state.Wrong, None),
        (state.Wrong, b"Hello, World!", state.Wrong, None),
        (state.Wrong, b'{"name": "John Doe", "age": 25}', state.Wrong, None),
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
    arrange_ctx = arrange_state(mock_context)
    arrange_handler = res.set_body_bytes(arrange_body)

    # act
    act_ctx = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body


@pytest.mark.parametrize(
    "arrange_state,arrange_body,assert_state,assert_body",
    [
        (state.Right, "", state.Right, b""),
        (state.Right, "Hello, World!", state.Right, b"Hello, World!"),
        (
            state.Right,
            '{"name": "John Doe", "age": 25}',
            state.Right,
            b'{"name": "John Doe", "age": 25}',
        ),
        (state.Wrong, "", state.Wrong, None),
        (state.Wrong, "Hello, World!", state.Wrong, None),
        (state.Wrong, '{"name": "John Doe", "age": 25}', state.Wrong, None),
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
    arrange_ctx = arrange_state(mock_context)
    arrange_handler = res.set_body_text(arrange_body)

    # act
    act_ctx = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body


# Common functions for dynamic body set
ERROR = Exception("Error Message")
BYTES_ERROR_MESSAGE = str(ERROR).encode("UTF-8")


def sync_set_right_concrete_body(data):  # noqa
    return lambda _: state.Right(data)


def sync_set_error_body(_):
    return state.Error(ERROR)


def async_set_right_concrete_body(data):  # noqa
    async def _handler(_):
        return state.Right(data)

    return _handler


async def async_set_error_body(_):  # noqa
    return state.Error(ERROR)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.Right, sync_set_right_concrete_body(b""), state.Right, b""),
        (state.Right, sync_set_right_concrete_body(b"ABCD"), state.Right, b"ABCD"),
        (
            state.Right,
            sync_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.Right,
            b'{"name": "John Doe"}',
        ),
        (state.Wrong, sync_set_right_concrete_body(b""), state.Wrong, None),
        (state.Wrong, sync_set_right_concrete_body(b"ABCD"), state.Wrong, None),
        (
            state.Wrong,
            sync_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.Wrong,
            None,
        ),
        (state.Right, async_set_right_concrete_body(b""), state.Right, b""),
        (state.Right, async_set_right_concrete_body(b"ABCD"), state.Right, b"ABCD"),
        (
            state.Right,
            async_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.Right,
            b'{"name": "John Doe"}',
        ),
        (state.Wrong, async_set_right_concrete_body(b""), state.Wrong, None),
        (state.Wrong, async_set_right_concrete_body(b"ABCD"), state.Wrong, None),
        (
            state.Wrong,
            async_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.Wrong,
            None,
        ),
        (
            state.Right,
            sync_set_error_body,
            state.Error,
            BYTES_ERROR_MESSAGE,
        ),
        (state.Right, async_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (state.Wrong, sync_set_error_body, state.Wrong, None),
        (state.Wrong, async_set_error_body, state.Wrong, None),
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
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_body_from_bytes(act_function)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.Right, sync_set_right_concrete_body({}), state.Right, b"{}"),  # noqa
        (
            state.Right,
            sync_set_right_concrete_body({"name": "John Doe"}),
            state.Right,
            b'{"name":"John Doe"}',
        ),
        (
            state.Right,
            sync_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.Right,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.Right, sync_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (state.Right, async_set_right_concrete_body({}), state.Right, b"{}"),  # noqa
        (
            state.Right,
            async_set_right_concrete_body({"name": "John Doe"}),
            state.Right,
            b'{"name":"John Doe"}',
        ),
        (
            state.Right,
            async_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.Right,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.Right, async_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (state.Wrong, sync_set_right_concrete_body({}), state.Wrong, None),  # noqa
        (
            state.Wrong,
            sync_set_right_concrete_body({"name": "John Doe"}),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            sync_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, sync_set_error_body, state.Wrong, None),
        (state.Wrong, async_set_right_concrete_body({}), state.Wrong, None),  # noqa
        (
            state.Wrong,
            async_set_right_concrete_body({"name": "John Doe"}),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            async_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, async_set_error_body, state.Wrong, None),
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
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_body_from_dict(act_function)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body


# Functions and classes for test-cases of `set_body_from_dict`


class User(pydantic.BaseModel):  # noqa
    name: str


class UserInfo(pydantic.BaseModel):  # noqa
    age: int
    city: str


class ExtendedUser(pydantic.BaseModel):  # noqa
    name: str
    info: UserInfo


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (
            state.Right,
            sync_set_right_concrete_body(pydantic.BaseModel()),
            state.Right,
            b"{}",  # noqa
        ),
        (
            state.Right,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.Right,
            b'{"name":"John Doe"}',
        ),
        (
            state.Right,
            sync_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.Right,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.Right, sync_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (
            state.Right,
            async_set_right_concrete_body(pydantic.BaseModel()),
            state.Right,
            b"{}",  # noqa
        ),
        (
            state.Right,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.Right,
            b'{"name":"John Doe"}',
        ),
        (
            state.Right,
            async_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.Right,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.Right, async_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        #
        (
            state.Wrong,
            sync_set_right_concrete_body(pydantic.BaseModel()),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            sync_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, sync_set_error_body, state.Wrong, None),
        (
            state.Wrong,
            async_set_right_concrete_body(pydantic.BaseModel()),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            async_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, async_set_error_body, state.Wrong, None),
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
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_body_from_pydantic(act_function)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.Right, sync_set_right_concrete_body(""), state.Right, b""),
        (
            state.Right,
            sync_set_right_concrete_body("Hello, World"),
            state.Right,
            b"Hello, World",
        ),
        (
            state.Right,
            sync_set_right_concrete_body('{"name": "John Doe"}'),
            state.Right,
            b'{"name": "John Doe"}',
        ),
        (
            state.Right,
            sync_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.Right,
            b'{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}',
        ),
        (state.Right, sync_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (state.Right, async_set_right_concrete_body(""), state.Right, b""),
        (
            state.Right,
            async_set_right_concrete_body("Hello, World"),
            state.Right,
            b"Hello, World",
        ),
        (
            state.Right,
            async_set_right_concrete_body('{"name": "John Doe"}'),
            state.Right,
            b'{"name": "John Doe"}',
        ),
        (
            state.Right,
            async_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.Right,
            b'{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}',
        ),
        (state.Right, async_set_error_body, state.Error, BYTES_ERROR_MESSAGE),
        (state.Wrong, sync_set_right_concrete_body(""), state.Wrong, None),
        (state.Wrong, sync_set_right_concrete_body("Hello, World"), state.Wrong, None),
        (
            state.Wrong,
            sync_set_right_concrete_body('{"name": "John Doe"}'),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            sync_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, sync_set_error_body, state.Wrong, None),
        (state.Wrong, async_set_right_concrete_body(""), state.Wrong, None),
        (state.Wrong, async_set_right_concrete_body("Hello, World"), state.Wrong, None),
        (
            state.Wrong,
            async_set_right_concrete_body('{"name": "John Doe"}'),
            state.Wrong,
            None,
        ),
        (
            state.Wrong,
            async_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.Wrong,
            None,
        ),
        (state.Wrong, async_set_error_body, state.Wrong, None),
    ],
)
async def test_set_body_from_text(
    mock_context: context.Context,
    arrange_state,
    act_function,
    assert_state,
    assert_body,
):
    # arrange
    arrange_ctx = future.from_value(arrange_state(mock_context))
    arrange_handler = res.set_body_from_text(act_function)

    # act
    act_ctx: context.StateContext = await (arrange_ctx >> arrange_handler)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.response.body == assert_body
