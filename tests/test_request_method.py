import pytest

from mona import req, types
from mona.monads import state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_method,assert_state",
    [
        # GET
        ("GET", state.Right, "GET", state.Right),
        ("POST", state.Right, "GET", state.Wrong),
        ("PATCH", state.Right, "GET", state.Wrong),
        ("PUT", state.Right, "GET", state.Wrong),
        ("DELETE", state.Right, "GET", state.Wrong),
        ("OPTIONS", state.Right, "GET", state.Wrong),
        ("HEAD", state.Right, "GET", state.Wrong),
        ("TRACE", state.Right, "GET", state.Wrong),
        ("CONNECT", state.Right, "GET", state.Wrong),
        ("GET", state.Wrong, "GET", state.Wrong),
        ("POST", state.Wrong, "GET", state.Wrong),
        ("PATCH", state.Wrong, "GET", state.Wrong),
        ("PUT", state.Wrong, "GET", state.Wrong),
        ("DELETE", state.Wrong, "GET", state.Wrong),
        ("OPTIONS", state.Wrong, "GET", state.Wrong),
        ("HEAD", state.Wrong, "GET", state.Wrong),
        ("TRACE", state.Wrong, "GET", state.Wrong),
        ("CONNECT", state.Wrong, "GET", state.Wrong),
        # POST
        ("GET", state.Right, "POST", state.Wrong),
        ("POST", state.Right, "POST", state.Right),
        ("PATCH", state.Right, "POST", state.Wrong),
        ("PUT", state.Right, "POST", state.Wrong),
        ("DELETE", state.Right, "POST", state.Wrong),
        ("OPTIONS", state.Right, "POST", state.Wrong),
        ("HEAD", state.Right, "POST", state.Wrong),
        ("TRACE", state.Right, "POST", state.Wrong),
        ("CONNECT", state.Right, "POST", state.Wrong),
        ("GET", state.Wrong, "POST", state.Wrong),
        ("POST", state.Wrong, "POST", state.Wrong),
        ("PATCH", state.Wrong, "POST", state.Wrong),
        ("PUT", state.Wrong, "POST", state.Wrong),
        ("DELETE", state.Wrong, "POST", state.Wrong),
        ("OPTIONS", state.Wrong, "POST", state.Wrong),
        ("HEAD", state.Wrong, "POST", state.Wrong),
        ("TRACE", state.Wrong, "POST", state.Wrong),
        ("CONNECT", state.Wrong, "POST", state.Wrong),
        # PATCH
        ("GET", state.Right, "PATCH", state.Wrong),
        ("POST", state.Right, "PATCH", state.Wrong),
        ("PATCH", state.Right, "PATCH", state.Right),
        ("PUT", state.Right, "PATCH", state.Wrong),
        ("DELETE", state.Right, "PATCH", state.Wrong),
        ("OPTIONS", state.Right, "PATCH", state.Wrong),
        ("HEAD", state.Right, "PATCH", state.Wrong),
        ("TRACE", state.Right, "PATCH", state.Wrong),
        ("CONNECT", state.Right, "PATCH", state.Wrong),
        ("GET", state.Wrong, "PATCH", state.Wrong),
        ("POST", state.Wrong, "PATCH", state.Wrong),
        ("PATCH", state.Wrong, "PATCH", state.Wrong),
        ("PUT", state.Wrong, "PATCH", state.Wrong),
        ("DELETE", state.Wrong, "PATCH", state.Wrong),
        ("OPTIONS", state.Wrong, "PATCH", state.Wrong),
        ("HEAD", state.Wrong, "PATCH", state.Wrong),
        ("TRACE", state.Wrong, "PATCH", state.Wrong),
        ("CONNECT", state.Wrong, "PATCH", state.Wrong),
        # PUT
        ("GET", state.Right, "PUT", state.Wrong),
        ("POST", state.Right, "PUT", state.Wrong),
        ("PATCH", state.Right, "PUT", state.Wrong),
        ("PUT", state.Right, "PUT", state.Right),
        ("DELETE", state.Right, "PUT", state.Wrong),
        ("OPTIONS", state.Right, "PUT", state.Wrong),
        ("HEAD", state.Right, "PUT", state.Wrong),
        ("TRACE", state.Right, "PUT", state.Wrong),
        ("CONNECT", state.Right, "PUT", state.Wrong),
        ("GET", state.Wrong, "PUT", state.Wrong),
        ("POST", state.Wrong, "PUT", state.Wrong),
        ("PATCH", state.Wrong, "PUT", state.Wrong),
        ("PUT", state.Wrong, "PUT", state.Wrong),
        ("DELETE", state.Wrong, "PUT", state.Wrong),
        ("OPTIONS", state.Wrong, "PUT", state.Wrong),
        ("HEAD", state.Wrong, "PUT", state.Wrong),
        ("TRACE", state.Wrong, "PUT", state.Wrong),
        ("CONNECT", state.Wrong, "PUT", state.Wrong),
        # DELETE
        ("GET", state.Right, "DELETE", state.Wrong),
        ("POST", state.Right, "DELETE", state.Wrong),
        ("PATCH", state.Right, "DELETE", state.Wrong),
        ("PUT", state.Right, "DELETE", state.Wrong),
        ("DELETE", state.Right, "DELETE", state.Right),
        ("OPTIONS", state.Right, "DELETE", state.Wrong),
        ("HEAD", state.Right, "DELETE", state.Wrong),
        ("TRACE", state.Right, "DELETE", state.Wrong),
        ("CONNECT", state.Right, "DELETE", state.Wrong),
        ("GET", state.Wrong, "DELETE", state.Wrong),
        ("POST", state.Wrong, "DELETE", state.Wrong),
        ("PATCH", state.Wrong, "DELETE", state.Wrong),
        ("PUT", state.Wrong, "DELETE", state.Wrong),
        ("DELETE", state.Wrong, "DELETE", state.Wrong),
        ("OPTIONS", state.Wrong, "DELETE", state.Wrong),
        ("HEAD", state.Wrong, "DELETE", state.Wrong),
        ("TRACE", state.Wrong, "DELETE", state.Wrong),
        ("CONNECT", state.Wrong, "DELETE", state.Wrong),
        # OPTIONS
        ("GET", state.Right, "OPTIONS", state.Wrong),
        ("POST", state.Right, "OPTIONS", state.Wrong),
        ("PATCH", state.Right, "OPTIONS", state.Wrong),
        ("PUT", state.Right, "OPTIONS", state.Wrong),
        ("DELETE", state.Right, "OPTIONS", state.Wrong),
        ("OPTIONS", state.Right, "OPTIONS", state.Right),
        ("HEAD", state.Right, "OPTIONS", state.Wrong),
        ("TRACE", state.Right, "OPTIONS", state.Wrong),
        ("CONNECT", state.Right, "OPTIONS", state.Wrong),
        ("GET", state.Wrong, "OPTIONS", state.Wrong),
        ("POST", state.Wrong, "OPTIONS", state.Wrong),
        ("PATCH", state.Wrong, "OPTIONS", state.Wrong),
        ("PUT", state.Wrong, "OPTIONS", state.Wrong),
        ("DELETE", state.Wrong, "OPTIONS", state.Wrong),
        ("OPTIONS", state.Wrong, "OPTIONS", state.Wrong),
        ("HEAD", state.Wrong, "OPTIONS", state.Wrong),
        ("TRACE", state.Wrong, "OPTIONS", state.Wrong),
        ("CONNECT", state.Wrong, "OPTIONS", state.Wrong),
        # HEAD
        ("GET", state.Right, "HEAD", state.Wrong),
        ("POST", state.Right, "HEAD", state.Wrong),
        ("PATCH", state.Right, "HEAD", state.Wrong),
        ("PUT", state.Right, "HEAD", state.Wrong),
        ("DELETE", state.Right, "HEAD", state.Wrong),
        ("OPTIONS", state.Right, "HEAD", state.Wrong),
        ("HEAD", state.Right, "HEAD", state.Right),
        ("TRACE", state.Right, "HEAD", state.Wrong),
        ("CONNECT", state.Right, "HEAD", state.Wrong),
        ("GET", state.Wrong, "HEAD", state.Wrong),
        ("POST", state.Wrong, "HEAD", state.Wrong),
        ("PATCH", state.Wrong, "HEAD", state.Wrong),
        ("PUT", state.Wrong, "HEAD", state.Wrong),
        ("DELETE", state.Wrong, "HEAD", state.Wrong),
        ("OPTIONS", state.Wrong, "HEAD", state.Wrong),
        ("HEAD", state.Wrong, "HEAD", state.Wrong),
        ("TRACE", state.Wrong, "HEAD", state.Wrong),
        ("CONNECT", state.Wrong, "HEAD", state.Wrong),
        # TRACE
        ("GET", state.Right, "TRACE", state.Wrong),
        ("POST", state.Right, "TRACE", state.Wrong),
        ("PATCH", state.Right, "TRACE", state.Wrong),
        ("PUT", state.Right, "TRACE", state.Wrong),
        ("DELETE", state.Right, "TRACE", state.Wrong),
        ("OPTIONS", state.Right, "TRACE", state.Wrong),
        ("HEAD", state.Right, "TRACE", state.Wrong),
        ("TRACE", state.Right, "TRACE", state.Right),
        ("CONNECT", state.Right, "TRACE", state.Wrong),
        ("GET", state.Wrong, "TRACE", state.Wrong),
        ("POST", state.Wrong, "TRACE", state.Wrong),
        ("PATCH", state.Wrong, "TRACE", state.Wrong),
        ("PUT", state.Wrong, "TRACE", state.Wrong),
        ("DELETE", state.Wrong, "TRACE", state.Wrong),
        ("OPTIONS", state.Wrong, "TRACE", state.Wrong),
        ("HEAD", state.Wrong, "TRACE", state.Wrong),
        ("TRACE", state.Wrong, "TRACE", state.Wrong),
        ("CONNECT", state.Wrong, "TRACE", state.Wrong),
        # CONNECT
        ("GET", state.Right, "CONNECT", state.Wrong),
        ("POST", state.Right, "CONNECT", state.Wrong),
        ("PATCH", state.Right, "CONNECT", state.Wrong),
        ("PUT", state.Right, "CONNECT", state.Wrong),
        ("DELETE", state.Right, "CONNECT", state.Wrong),
        ("OPTIONS", state.Right, "CONNECT", state.Wrong),
        ("HEAD", state.Right, "CONNECT", state.Wrong),
        ("TRACE", state.Right, "CONNECT", state.Wrong),
        ("CONNECT", state.Right, "CONNECT", state.Right),
        ("GET", state.Wrong, "CONNECT", state.Wrong),
        ("POST", state.Wrong, "CONNECT", state.Wrong),
        ("PATCH", state.Wrong, "CONNECT", state.Wrong),
        ("PUT", state.Wrong, "CONNECT", state.Wrong),
        ("DELETE", state.Wrong, "CONNECT", state.Wrong),
        ("OPTIONS", state.Wrong, "CONNECT", state.Wrong),
        ("HEAD", state.Wrong, "CONNECT", state.Wrong),
        ("TRACE", state.Wrong, "CONNECT", state.Wrong),
        ("CONNECT", state.Wrong, "CONNECT", state.Wrong),
    ],
)
def test_on_method(
    mock_context: types.Context,
    arrange_state: str,
    arrange_method: str,
    assert_method: str,
    assert_state: str,
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)
    arrange_handler = req.on_method(assert_method)

    # act
    act_ctx: types.StateContext = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Right),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_get(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_get(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Right),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_post(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_post(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Right),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_patch(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_patch(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Right),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_put(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_put(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Right),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_delete(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_delete(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Right),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_options(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_options(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Right),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_head(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_head(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Right),
        ("CONNECT", state.Right, state.Wrong),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_trace(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_trace(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.Right, state.Wrong),
        ("POST", state.Right, state.Wrong),
        ("PATCH", state.Right, state.Wrong),
        ("PUT", state.Right, state.Wrong),
        ("DELETE", state.Right, state.Wrong),
        ("OPTIONS", state.Right, state.Wrong),
        ("HEAD", state.Right, state.Wrong),
        ("TRACE", state.Right, state.Wrong),
        ("CONNECT", state.Right, state.Right),
        ("GET", state.Wrong, state.Wrong),
        ("POST", state.Wrong, state.Wrong),
        ("PATCH", state.Wrong, state.Wrong),
        ("PUT", state.Wrong, state.Wrong),
        ("DELETE", state.Wrong, state.Wrong),
        ("OPTIONS", state.Wrong, state.Wrong),
        ("HEAD", state.Wrong, state.Wrong),
        ("TRACE", state.Wrong, state.Wrong),
        ("CONNECT", state.Wrong, state.Wrong),
    ],
)
def test_on_connect(
    mock_context: types.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    arrange_ctx = arrange_state(mock_context)

    # act
    act_ctx: types.StateContext = req.on_connect(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
