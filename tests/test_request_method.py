import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "request_method,target_method,valid",
    [
        ("GET", "GET", True),
        ("POST", "GET", False),
        ("GET", "POST", False),
        ("SOME", "LOL", False),
        ("POST", "POST", True),
    ],
)
def test_on_method(
    asgi_context: context.Context, request_method: str, target_method: str, valid: bool
):
    asgi_context.method = request_method
    handler_ = req.on_method(target_method)

    ctx: context.StateContext = handler_(asgi_context)

    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", True),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_get(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_get(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", True),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_post(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_post(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", True),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_patch(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_patch(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", True),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_put(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_put(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", True),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_delete(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_delete(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", True),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_options(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_options(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", True),
        ("TRACE", False),
        ("CONNECT", False),
    ],
)
def test_on_head(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_head(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", True),
        ("CONNECT", False),
    ],
)
def test_on_trace(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_trace(asgi_context)
    assert state.is_valid(ctx) is valid


@pytest.mark.parametrize(
    "request_method,valid",
    [
        ("GET", False),
        ("POST", False),
        ("PATCH", False),
        ("PUT", False),
        ("DELETE", False),
        ("OPTIONS", False),
        ("HEAD", False),
        ("TRACE", False),
        ("CONNECT", True),
    ],
)
def test_on_connect(asgi_context: context.Context, request_method: str, valid: bool):
    asgi_context.method = request_method
    ctx: context.StateContext = req.on_connect(asgi_context)
    assert state.is_valid(ctx) is valid
