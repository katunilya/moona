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


# Common functions for dynamic body set
ERROR_MESSAGE = "Error Message"
BYTES_ERROR_MESSAGE = ERROR_MESSAGE.encode("UTF-8")


def sync_set_right_concrete_body(data):  # noqa
    return lambda _: state.right(data)


def sync_set_error_body(_):
    return state.error(error.Error(ERROR_MESSAGE))


def async_set_right_concrete_body(data):  # noqa
    async def _handler(_):
        return state.right(data)

    return _handler


async def async_set_error_body(_):  # noqa
    return state.error(error.Error(ERROR_MESSAGE))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.RIGHT, sync_set_right_concrete_body(b""), state.RIGHT, b""),
        (state.RIGHT, sync_set_right_concrete_body(b"ABCD"), state.RIGHT, b"ABCD"),
        (
            state.RIGHT,
            sync_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (state.WRONG, sync_set_right_concrete_body(b""), state.WRONG, None),
        (state.WRONG, sync_set_right_concrete_body(b"ABCD"), state.WRONG, None),
        (
            state.WRONG,
            sync_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (state.RIGHT, async_set_right_concrete_body(b""), state.RIGHT, b""),
        (state.RIGHT, async_set_right_concrete_body(b"ABCD"), state.RIGHT, b"ABCD"),
        (
            state.RIGHT,
            async_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (state.WRONG, async_set_right_concrete_body(b""), state.WRONG, None),
        (state.WRONG, async_set_right_concrete_body(b"ABCD"), state.WRONG, None),
        (
            state.WRONG,
            async_set_right_concrete_body(b'{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (
            state.RIGHT,
            sync_set_error_body,
            state.ERROR,
            BYTES_ERROR_MESSAGE,
        ),
        (state.RIGHT, async_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (state.WRONG, sync_set_error_body, state.WRONG, None),
        (state.WRONG, async_set_error_body, state.WRONG, None),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.RIGHT, sync_set_right_concrete_body({}), state.RIGHT, b"{}"),  # noqa
        (
            state.RIGHT,
            sync_set_right_concrete_body({"name": "John Doe"}),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.RIGHT, sync_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (state.RIGHT, async_set_right_concrete_body({}), state.RIGHT, b"{}"),  # noqa
        (
            state.RIGHT,
            async_set_right_concrete_body({"name": "John Doe"}),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            async_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.RIGHT, async_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (state.WRONG, sync_set_right_concrete_body({}), state.WRONG, None),  # noqa
        (
            state.WRONG,
            sync_set_right_concrete_body({"name": "John Doe"}),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, sync_set_error_body, state.WRONG, None),
        (state.WRONG, async_set_right_concrete_body({}), state.WRONG, None),  # noqa
        (
            state.WRONG,
            async_set_right_concrete_body({"name": "John Doe"}),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            async_set_right_concrete_body(
                {"name": "John Doe", "info": {"age": 21, "city": "SPb"}}
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, async_set_error_body, state.WRONG, None),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (
            state.RIGHT,
            sync_set_right_concrete_body(pydantic.BaseModel()),
            state.RIGHT,
            b"{}",  # noqa
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.RIGHT, sync_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (
            state.RIGHT,
            async_set_right_concrete_body(pydantic.BaseModel()),
            state.RIGHT,
            b"{}",  # noqa
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.RIGHT,
            b'{"name":"John Doe"}',
        ),
        (
            state.RIGHT,
            async_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.RIGHT,
            b'{"name":"John Doe","info":{"age":21,"city":"SPb"}}',
        ),
        (state.RIGHT, async_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        #
        (
            state.WRONG,
            sync_set_right_concrete_body(pydantic.BaseModel()),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, sync_set_error_body, state.WRONG, None),
        (
            state.WRONG,
            async_set_right_concrete_body(pydantic.BaseModel()),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_body(User(name="John Doe")),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            async_set_right_concrete_body(
                ExtendedUser(name="John Doe", info=UserInfo(age=21, city="SPb"))
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, async_set_error_body, state.WRONG, None),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_state,act_function,assert_state,assert_body",
    [
        (state.RIGHT, sync_set_right_concrete_body(""), state.RIGHT, b""),
        (
            state.RIGHT,
            sync_set_right_concrete_body("Hello, World"),
            state.RIGHT,
            b"Hello, World",
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body('{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (
            state.RIGHT,
            sync_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.RIGHT,
            b'{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}',
        ),
        (state.RIGHT, sync_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (state.RIGHT, async_set_right_concrete_body(""), state.RIGHT, b""),
        (
            state.RIGHT,
            async_set_right_concrete_body("Hello, World"),
            state.RIGHT,
            b"Hello, World",
        ),
        (
            state.RIGHT,
            async_set_right_concrete_body('{"name": "John Doe"}'),
            state.RIGHT,
            b'{"name": "John Doe"}',
        ),
        (
            state.RIGHT,
            async_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.RIGHT,
            b'{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}',
        ),
        (state.RIGHT, async_set_error_body, state.ERROR, BYTES_ERROR_MESSAGE),
        (state.WRONG, sync_set_right_concrete_body(""), state.WRONG, None),
        (state.WRONG, sync_set_right_concrete_body("Hello, World"), state.WRONG, None),
        (
            state.WRONG,
            sync_set_right_concrete_body('{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            sync_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, sync_set_error_body, state.WRONG, None),
        (state.WRONG, async_set_right_concrete_body(""), state.WRONG, None),
        (state.WRONG, async_set_right_concrete_body("Hello, World"), state.WRONG, None),
        (
            state.WRONG,
            async_set_right_concrete_body('{"name": "John Doe"}'),
            state.WRONG,
            None,
        ),
        (
            state.WRONG,
            async_set_right_concrete_body(
                '{"name": "John Doe", "info": {"age": 21, "city": "SPb"}}'
            ),
            state.WRONG,
            None,
        ),
        (state.WRONG, async_set_error_body, state.WRONG, None),
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
    ctx = future.from_value(state.pack(arrange_state, mock_context))
    handler = res.set_body_from_text(act_function)

    # act
    ctx: context.StateContext = await (ctx >> handler)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.response.body == assert_body
