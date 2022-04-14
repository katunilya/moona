import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_method,assert_state",
    [
        # GET
        ("GET", state.RIGHT, "GET", state.RIGHT),
        ("POST", state.RIGHT, "GET", state.WRONG),
        ("PATCH", state.RIGHT, "GET", state.WRONG),
        ("PUT", state.RIGHT, "GET", state.WRONG),
        ("DELETE", state.RIGHT, "GET", state.WRONG),
        ("OPTIONS", state.RIGHT, "GET", state.WRONG),
        ("HEAD", state.RIGHT, "GET", state.WRONG),
        ("TRACE", state.RIGHT, "GET", state.WRONG),
        ("CONNECT", state.RIGHT, "GET", state.WRONG),
        ("GET", state.WRONG, "GET", state.WRONG),
        ("POST", state.WRONG, "GET", state.WRONG),
        ("PATCH", state.WRONG, "GET", state.WRONG),
        ("PUT", state.WRONG, "GET", state.WRONG),
        ("DELETE", state.WRONG, "GET", state.WRONG),
        ("OPTIONS", state.WRONG, "GET", state.WRONG),
        ("HEAD", state.WRONG, "GET", state.WRONG),
        ("TRACE", state.WRONG, "GET", state.WRONG),
        ("CONNECT", state.WRONG, "GET", state.WRONG),
        # POST
        ("GET", state.RIGHT, "POST", state.WRONG),
        ("POST", state.RIGHT, "POST", state.RIGHT),
        ("PATCH", state.RIGHT, "POST", state.WRONG),
        ("PUT", state.RIGHT, "POST", state.WRONG),
        ("DELETE", state.RIGHT, "POST", state.WRONG),
        ("OPTIONS", state.RIGHT, "POST", state.WRONG),
        ("HEAD", state.RIGHT, "POST", state.WRONG),
        ("TRACE", state.RIGHT, "POST", state.WRONG),
        ("CONNECT", state.RIGHT, "POST", state.WRONG),
        ("GET", state.WRONG, "POST", state.WRONG),
        ("POST", state.WRONG, "POST", state.WRONG),
        ("PATCH", state.WRONG, "POST", state.WRONG),
        ("PUT", state.WRONG, "POST", state.WRONG),
        ("DELETE", state.WRONG, "POST", state.WRONG),
        ("OPTIONS", state.WRONG, "POST", state.WRONG),
        ("HEAD", state.WRONG, "POST", state.WRONG),
        ("TRACE", state.WRONG, "POST", state.WRONG),
        ("CONNECT", state.WRONG, "POST", state.WRONG),
        # PATCH
        ("GET", state.RIGHT, "PATCH", state.WRONG),
        ("POST", state.RIGHT, "PATCH", state.WRONG),
        ("PATCH", state.RIGHT, "PATCH", state.RIGHT),
        ("PUT", state.RIGHT, "PATCH", state.WRONG),
        ("DELETE", state.RIGHT, "PATCH", state.WRONG),
        ("OPTIONS", state.RIGHT, "PATCH", state.WRONG),
        ("HEAD", state.RIGHT, "PATCH", state.WRONG),
        ("TRACE", state.RIGHT, "PATCH", state.WRONG),
        ("CONNECT", state.RIGHT, "PATCH", state.WRONG),
        ("GET", state.WRONG, "PATCH", state.WRONG),
        ("POST", state.WRONG, "PATCH", state.WRONG),
        ("PATCH", state.WRONG, "PATCH", state.WRONG),
        ("PUT", state.WRONG, "PATCH", state.WRONG),
        ("DELETE", state.WRONG, "PATCH", state.WRONG),
        ("OPTIONS", state.WRONG, "PATCH", state.WRONG),
        ("HEAD", state.WRONG, "PATCH", state.WRONG),
        ("TRACE", state.WRONG, "PATCH", state.WRONG),
        ("CONNECT", state.WRONG, "PATCH", state.WRONG),
        # PUT
        ("GET", state.RIGHT, "PUT", state.WRONG),
        ("POST", state.RIGHT, "PUT", state.WRONG),
        ("PATCH", state.RIGHT, "PUT", state.WRONG),
        ("PUT", state.RIGHT, "PUT", state.RIGHT),
        ("DELETE", state.RIGHT, "PUT", state.WRONG),
        ("OPTIONS", state.RIGHT, "PUT", state.WRONG),
        ("HEAD", state.RIGHT, "PUT", state.WRONG),
        ("TRACE", state.RIGHT, "PUT", state.WRONG),
        ("CONNECT", state.RIGHT, "PUT", state.WRONG),
        ("GET", state.WRONG, "PUT", state.WRONG),
        ("POST", state.WRONG, "PUT", state.WRONG),
        ("PATCH", state.WRONG, "PUT", state.WRONG),
        ("PUT", state.WRONG, "PUT", state.WRONG),
        ("DELETE", state.WRONG, "PUT", state.WRONG),
        ("OPTIONS", state.WRONG, "PUT", state.WRONG),
        ("HEAD", state.WRONG, "PUT", state.WRONG),
        ("TRACE", state.WRONG, "PUT", state.WRONG),
        ("CONNECT", state.WRONG, "PUT", state.WRONG),
        # DELETE
        ("GET", state.RIGHT, "DELETE", state.WRONG),
        ("POST", state.RIGHT, "DELETE", state.WRONG),
        ("PATCH", state.RIGHT, "DELETE", state.WRONG),
        ("PUT", state.RIGHT, "DELETE", state.WRONG),
        ("DELETE", state.RIGHT, "DELETE", state.RIGHT),
        ("OPTIONS", state.RIGHT, "DELETE", state.WRONG),
        ("HEAD", state.RIGHT, "DELETE", state.WRONG),
        ("TRACE", state.RIGHT, "DELETE", state.WRONG),
        ("CONNECT", state.RIGHT, "DELETE", state.WRONG),
        ("GET", state.WRONG, "DELETE", state.WRONG),
        ("POST", state.WRONG, "DELETE", state.WRONG),
        ("PATCH", state.WRONG, "DELETE", state.WRONG),
        ("PUT", state.WRONG, "DELETE", state.WRONG),
        ("DELETE", state.WRONG, "DELETE", state.WRONG),
        ("OPTIONS", state.WRONG, "DELETE", state.WRONG),
        ("HEAD", state.WRONG, "DELETE", state.WRONG),
        ("TRACE", state.WRONG, "DELETE", state.WRONG),
        ("CONNECT", state.WRONG, "DELETE", state.WRONG),
        # OPTIONS
        ("GET", state.RIGHT, "OPTIONS", state.WRONG),
        ("POST", state.RIGHT, "OPTIONS", state.WRONG),
        ("PATCH", state.RIGHT, "OPTIONS", state.WRONG),
        ("PUT", state.RIGHT, "OPTIONS", state.WRONG),
        ("DELETE", state.RIGHT, "OPTIONS", state.WRONG),
        ("OPTIONS", state.RIGHT, "OPTIONS", state.RIGHT),
        ("HEAD", state.RIGHT, "OPTIONS", state.WRONG),
        ("TRACE", state.RIGHT, "OPTIONS", state.WRONG),
        ("CONNECT", state.RIGHT, "OPTIONS", state.WRONG),
        ("GET", state.WRONG, "OPTIONS", state.WRONG),
        ("POST", state.WRONG, "OPTIONS", state.WRONG),
        ("PATCH", state.WRONG, "OPTIONS", state.WRONG),
        ("PUT", state.WRONG, "OPTIONS", state.WRONG),
        ("DELETE", state.WRONG, "OPTIONS", state.WRONG),
        ("OPTIONS", state.WRONG, "OPTIONS", state.WRONG),
        ("HEAD", state.WRONG, "OPTIONS", state.WRONG),
        ("TRACE", state.WRONG, "OPTIONS", state.WRONG),
        ("CONNECT", state.WRONG, "OPTIONS", state.WRONG),
        # HEAD
        ("GET", state.RIGHT, "HEAD", state.WRONG),
        ("POST", state.RIGHT, "HEAD", state.WRONG),
        ("PATCH", state.RIGHT, "HEAD", state.WRONG),
        ("PUT", state.RIGHT, "HEAD", state.WRONG),
        ("DELETE", state.RIGHT, "HEAD", state.WRONG),
        ("OPTIONS", state.RIGHT, "HEAD", state.WRONG),
        ("HEAD", state.RIGHT, "HEAD", state.RIGHT),
        ("TRACE", state.RIGHT, "HEAD", state.WRONG),
        ("CONNECT", state.RIGHT, "HEAD", state.WRONG),
        ("GET", state.WRONG, "HEAD", state.WRONG),
        ("POST", state.WRONG, "HEAD", state.WRONG),
        ("PATCH", state.WRONG, "HEAD", state.WRONG),
        ("PUT", state.WRONG, "HEAD", state.WRONG),
        ("DELETE", state.WRONG, "HEAD", state.WRONG),
        ("OPTIONS", state.WRONG, "HEAD", state.WRONG),
        ("HEAD", state.WRONG, "HEAD", state.WRONG),
        ("TRACE", state.WRONG, "HEAD", state.WRONG),
        ("CONNECT", state.WRONG, "HEAD", state.WRONG),
        # TRACE
        ("GET", state.RIGHT, "TRACE", state.WRONG),
        ("POST", state.RIGHT, "TRACE", state.WRONG),
        ("PATCH", state.RIGHT, "TRACE", state.WRONG),
        ("PUT", state.RIGHT, "TRACE", state.WRONG),
        ("DELETE", state.RIGHT, "TRACE", state.WRONG),
        ("OPTIONS", state.RIGHT, "TRACE", state.WRONG),
        ("HEAD", state.RIGHT, "TRACE", state.WRONG),
        ("TRACE", state.RIGHT, "TRACE", state.RIGHT),
        ("CONNECT", state.RIGHT, "TRACE", state.WRONG),
        ("GET", state.WRONG, "TRACE", state.WRONG),
        ("POST", state.WRONG, "TRACE", state.WRONG),
        ("PATCH", state.WRONG, "TRACE", state.WRONG),
        ("PUT", state.WRONG, "TRACE", state.WRONG),
        ("DELETE", state.WRONG, "TRACE", state.WRONG),
        ("OPTIONS", state.WRONG, "TRACE", state.WRONG),
        ("HEAD", state.WRONG, "TRACE", state.WRONG),
        ("TRACE", state.WRONG, "TRACE", state.WRONG),
        ("CONNECT", state.WRONG, "TRACE", state.WRONG),
        # CONNECT
        ("GET", state.RIGHT, "CONNECT", state.WRONG),
        ("POST", state.RIGHT, "CONNECT", state.WRONG),
        ("PATCH", state.RIGHT, "CONNECT", state.WRONG),
        ("PUT", state.RIGHT, "CONNECT", state.WRONG),
        ("DELETE", state.RIGHT, "CONNECT", state.WRONG),
        ("OPTIONS", state.RIGHT, "CONNECT", state.WRONG),
        ("HEAD", state.RIGHT, "CONNECT", state.WRONG),
        ("TRACE", state.RIGHT, "CONNECT", state.WRONG),
        ("CONNECT", state.RIGHT, "CONNECT", state.RIGHT),
        ("GET", state.WRONG, "CONNECT", state.WRONG),
        ("POST", state.WRONG, "CONNECT", state.WRONG),
        ("PATCH", state.WRONG, "CONNECT", state.WRONG),
        ("PUT", state.WRONG, "CONNECT", state.WRONG),
        ("DELETE", state.WRONG, "CONNECT", state.WRONG),
        ("OPTIONS", state.WRONG, "CONNECT", state.WRONG),
        ("HEAD", state.WRONG, "CONNECT", state.WRONG),
        ("TRACE", state.WRONG, "CONNECT", state.WRONG),
        ("CONNECT", state.WRONG, "CONNECT", state.WRONG),
    ],
)
def test_on_method(
    mock_context: context.Context,
    arrange_state: str,
    arrange_method: str,
    assert_method: str,
    assert_state: str,
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)
    handler_ = req.on_method(assert_method)

    # act
    ctx: context.StateContext = handler_(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.RIGHT),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_get(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_get(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.RIGHT),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_post(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_post(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.RIGHT),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_patch(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_patch(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.RIGHT),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_put(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_put(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.RIGHT),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_delete(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_delete(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.RIGHT),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_options(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_options(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.RIGHT),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_head(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_head(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.RIGHT),
        ("CONNECT", state.RIGHT, state.WRONG),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_trace(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_trace(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_method,arrange_state,assert_state",
    [
        ("GET", state.RIGHT, state.WRONG),
        ("POST", state.RIGHT, state.WRONG),
        ("PATCH", state.RIGHT, state.WRONG),
        ("PUT", state.RIGHT, state.WRONG),
        ("DELETE", state.RIGHT, state.WRONG),
        ("OPTIONS", state.RIGHT, state.WRONG),
        ("HEAD", state.RIGHT, state.WRONG),
        ("TRACE", state.RIGHT, state.WRONG),
        ("CONNECT", state.RIGHT, state.RIGHT),
        ("GET", state.WRONG, state.WRONG),
        ("POST", state.WRONG, state.WRONG),
        ("PATCH", state.WRONG, state.WRONG),
        ("PUT", state.WRONG, state.WRONG),
        ("DELETE", state.WRONG, state.WRONG),
        ("OPTIONS", state.WRONG, state.WRONG),
        ("HEAD", state.WRONG, state.WRONG),
        ("TRACE", state.WRONG, state.WRONG),
        ("CONNECT", state.WRONG, state.WRONG),
    ],
)
def test_on_connect(
    mock_context: context.Context, arrange_method, arrange_state, assert_state
):
    # arrange
    mock_context.request.method = arrange_method
    ctx = state.pack(arrange_state, mock_context)

    # act
    ctx: context.StateContext = req.on_connect(ctx)

    # assert
    assert ctx.state == assert_state
