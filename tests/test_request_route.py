import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "path,pattern,valid",
    [
        ("path", "path", True),
        ("path", "/path", True),
        ("path", "path/", True),
        ("path", "/path/", True),
        ("path", "paths", False),
        ("path", "/paths", False),
        ("path", "paths/", False),
        ("path", "/paths/", False),
        ("some/path", "some/path", True),
        ("some/path", "/some/path", True),
        ("some/path", "some/path/", True),
        ("some/path", "/some/path/", True),
        ("some/path", "somes/path", False),
        ("some/path", "/somes/path", False),
        ("some/path", "somes/path/", False),
        ("some/path", "/somes/path/", False),
        ("some/path", "some/paath", False),
        ("some/path", "/some/paath", False),
        ("some/path", "some/paath/", False),
        ("some/path", "/some/paath/", False),
        ("some/path", "x/some/path", False),
        ("some/path", "some/path/x", False),
        ("some/path", "x/some/path/x", False),
    ],
)
def test_on_route(asgi_context: context.Context, path: str, pattern: str, valid: bool):
    asgi_context.path = path.strip("/")
    handler = req.on_route(pattern)

    ctx: context.StateContext = handler(asgi_context)

    assert state.is_valid(ctx) == valid


@pytest.mark.parametrize(
    "path,pattern,valid,afterpath",
    [
        ("subroute/path", "subroute", True, "path"),
        ("subroute/path", "subroute/", True, "path"),
        ("subroute/path", "/subroute", True, "path"),
        ("subroute/path", "/subroute/", True, "path"),
        ("subroute/path", "subroutes", False, "subroute/path"),
        ("subroute/path", "subroutes/", False, "subroute/path"),
        ("subroute/path", "/subroutes", False, "subroute/path"),
        ("subroute/path", "/subroutes/", False, "subroute/path"),
    ],
)
def test_on_subroute(
    asgi_context: context.Context, path: str, pattern: str, valid: bool, afterpath: str
):
    asgi_context.path = path
    handle = req.on_subroute(pattern)

    ctx: context.StateContext = handle(asgi_context)

    assert state.is_valid(ctx) == valid
    assert ctx.value.path == afterpath


@pytest.mark.parametrize(
    "path,pattern,valid",
    [
        ("path", "path", True),
        ("path", "/path", True),
        ("path", "path/", True),
        ("path", "/path/", True),
        ("path", "paths", False),
        ("path", "/paths", False),
        ("path", "paths/", False),
        ("path", "/paths/", False),
        ("some/path", "some/path", True),
        ("some/path", "/some/path", True),
        ("some/path", "some/path/", True),
        ("some/path", "/some/path/", True),
        ("some/path", "somes/path", False),
        ("some/path", "/somes/path", False),
        ("some/path", "somes/path/", False),
        ("some/path", "/somes/path/", False),
        ("some/path", "some/paath", False),
        ("some/path", "/some/paath", False),
        ("some/path", "some/paath/", False),
        ("some/path", "/some/paath/", False),
        ("some/path", "x/some/path", False),
        ("some/path", "some/path/x", False),
        ("some/path", "x/some/path/x", False),
        ("Path", "path", True),
        ("Path", "/path", True),
        ("Path", "path/", True),
        ("Path", "/path/", True),
        ("Path", "paths", False),
        ("Path", "/paths", False),
        ("Path", "paths/", False),
        ("Path", "/paths/", False),
        ("sOme/path", "some/path", True),
        ("sOme/path", "/some/path", True),
        ("sOme/path", "some/path/", True),
        ("sOme/path", "/some/path/", True),
        ("sOme/path", "somes/path", False),
        ("sOme/path", "/somes/path", False),
        ("sOme/path", "somes/path/", False),
        ("sOme/path", "/somes/path/", False),
        ("sOme/path", "some/paath", False),
        ("sOme/path", "/some/paath", False),
        ("sOme/path", "some/paath/", False),
        ("sOme/path", "/some/paath/", False),
        ("sOme/path", "x/some/path", False),
        ("sOme/path", "some/path/x", False),
        ("sOme/path", "x/some/path/x", False),
        ("Path", "/pAth", True),
        ("Path", "pAth/", True),
        ("Path", "/pAth/", True),
        ("Path", "pAths", False),
        ("Path", "/pAths", False),
        ("Path", "pAths/", False),
        ("Path", "/pAths/", False),
        ("sOme/path", "some/patH", True),
        ("sOme/path", "/some/patH", True),
        ("sOme/path", "some/patH/", True),
        ("sOme/path", "/some/patH/", True),
        ("sOme/path", "somes/patH", False),
        ("sOme/path", "/somes/patH", False),
        ("sOme/path", "somes/patH/", False),
        ("sOme/path", "/somes/patH/", False),
        ("sOme/path", "some/paatH", False),
        ("sOme/path", "/some/paatH", False),
        ("sOme/path", "some/paatH/", False),
        ("sOme/path", "/some/paatH/", False),
        ("sOme/path", "x/some/patH", False),
        ("sOme/path", "some/patH/x", False),
        ("sOme/path", "x/some/patH/x", False),
    ],
)
def test_on_ciroute(
    asgi_context: context.Context, path: str, pattern: str, valid: bool
):
    asgi_context.path = path.strip("/")
    handler = req.on_ciroute(pattern)

    ctx: context.StateContext = handler(asgi_context)

    assert state.is_valid(ctx) == valid


@pytest.mark.parametrize(
    "path,pattern,valid,afterpath",
    [
        ("subroute/path", "subroute", True, "path"),
        ("subroute/path", "subroute/", True, "path"),
        ("subroute/path", "/subroute", True, "path"),
        ("subroute/path", "/subroute/", True, "path"),
        ("subroute/path", "subroutes", False, "subroute/path"),
        ("subroute/path", "subroutes/", False, "subroute/path"),
        ("subroute/path", "/subroutes", False, "subroute/path"),
        ("subroute/path", "/subroutes/", False, "subroute/path"),
        ("Subroute/path", "subroute", True, "path"),
        ("Subroute/path", "subroute/", True, "path"),
        ("Subroute/path", "/subroute", True, "path"),
        ("Subroute/path", "/subroute/", True, "path"),
        ("Subroute/path", "subroutes", False, "Subroute/path"),
        ("Subroute/path", "subroutes/", False, "Subroute/path"),
        ("Subroute/path", "/subroutes", False, "Subroute/path"),
        ("Subroute/path", "/subroutes/", False, "Subroute/path"),
        ("subroute/path", "/subroutes/", False, "subroute/path"),
        ("Subroute/path", "suBroute", True, "path"),
        ("Subroute/path", "suBroute/", True, "path"),
        ("Subroute/path", "/suBroute", True, "path"),
        ("Subroute/path", "/suBroute/", True, "path"),
        ("Subroute/path", "suBroutes", False, "Subroute/path"),
        ("Subroute/path", "suBroutes/", False, "Subroute/path"),
        ("Subroute/path", "/suBroutes", False, "Subroute/path"),
        ("Subroute/path", "/suBroutes/", False, "Subroute/path"),
    ],
)
def test_on_cisubroute(
    asgi_context: context.Context, path: str, pattern: str, valid: bool, afterpath: str
):
    asgi_context.path = path
    handle = req.on_cisubroute(pattern)

    ctx: context.StateContext = handle(asgi_context)

    assert state.is_valid(ctx) == valid
    assert ctx.value.path == afterpath
