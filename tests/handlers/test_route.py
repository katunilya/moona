import pytest

from moona.context import HTTPContext
from moona.handlers.route import WrongPathError, ci_route, ci_subroute, route, subroute


@pytest.mark.parametrize(
    "ctx_path, path, result_type",
    [
        ("path", "path", HTTPContext),
        ("path", "/path", HTTPContext),
        ("path", "path/", HTTPContext),
        ("path", "/path/", HTTPContext),
        ("path", "paths", WrongPathError),
        ("path", "/paths", WrongPathError),
        ("path", "paths/", WrongPathError),
        ("path", "/paths/", WrongPathError),
        ("some/path", "some/path", HTTPContext),
        ("some/path", "/some/path", HTTPContext),
        ("some/path", "some/path/", HTTPContext),
        ("some/path", "/some/path/", HTTPContext),
        ("some/path", "somes/path", WrongPathError),
        ("some/path", "/somes/path", WrongPathError),
        ("some/path", "somes/path/", WrongPathError),
        ("some/path", "/somes/path/", WrongPathError),
        ("some/path", "some/paath", WrongPathError),
        ("some/path", "/some/paath", WrongPathError),
        ("some/path", "some/paath/", WrongPathError),
        ("some/path", "/some/paath/", WrongPathError),
        ("some/path", "x/some/path", WrongPathError),
        ("some/path", "some/path/x", WrongPathError),
        ("some/path", "x/some/path/x", WrongPathError),
    ],
)
def test_route(ctx: HTTPContext, ctx_path, path, result_type):
    ctx.request.path = ctx_path
    assert isinstance(
        ctx >> route(path),
        result_type,
    )


@pytest.mark.parametrize(
    "ctx_path, path, result_path, result_type",
    [
        ("subroute/path", "subroute", "path", HTTPContext),
        ("subroute/path", "subroute/", "path", HTTPContext),
        ("subroute/path", "/subroute", "path", HTTPContext),
        ("subroute/path", "/subroute/", "path", HTTPContext),
        ("subroute/path", "subroutes", "subroute/path", WrongPathError),
        ("subroute/path", "subroutes/", "subroute/path", WrongPathError),
        ("subroute/path", "/subroutes", "subroute/path", WrongPathError),
        ("subroute/path", "/subroutes/", "subroute/path", WrongPathError),
    ],
)
def test_subroute(ctx: HTTPContext, ctx_path, path, result_path, result_type):
    ctx.request.path = ctx_path
    result = ctx >> subroute(path)
    match result:
        case HTTPContext():
            assert result.request.path == result_path
        case WrongPathError():
            assert isinstance(result, result_type)


@pytest.mark.parametrize(
    "ctx_path, path, result_type",
    [
        ("path", "path", HTTPContext),
        ("path", "/path", HTTPContext),
        ("path", "path/", HTTPContext),
        ("path", "/path/", HTTPContext),
        ("path", "paths", WrongPathError),
        ("path", "/paths", WrongPathError),
        ("path", "paths/", WrongPathError),
        ("path", "/paths/", WrongPathError),
        ("some/path", "some/path", HTTPContext),
        ("some/path", "/some/path", HTTPContext),
        ("some/path", "some/path/", HTTPContext),
        ("some/path", "/some/path/", HTTPContext),
        ("some/path", "somes/path", WrongPathError),
        ("some/path", "/somes/path", WrongPathError),
        ("some/path", "somes/path/", WrongPathError),
        ("some/path", "/somes/path/", WrongPathError),
        ("some/path", "some/paath", WrongPathError),
        ("some/path", "/some/paath", WrongPathError),
        ("some/path", "some/paath/", WrongPathError),
        ("some/path", "/some/paath/", WrongPathError),
        ("some/path", "x/some/path", WrongPathError),
        ("some/path", "some/path/x", WrongPathError),
        ("some/path", "x/some/path/x", WrongPathError),
        ("Path", "path", HTTPContext),
        ("Path", "/path", HTTPContext),
        ("Path", "path/", HTTPContext),
        ("Path", "/path/", HTTPContext),
        ("Path", "paths", WrongPathError),
        ("Path", "/paths", WrongPathError),
        ("Path", "paths/", WrongPathError),
        ("Path", "/paths/", WrongPathError),
        ("Some/path", "some/path", HTTPContext),
        ("Some/path", "/some/path", HTTPContext),
        ("Some/path", "some/path/", HTTPContext),
        ("Some/path", "/some/path/", HTTPContext),
        ("Some/path", "somes/path", WrongPathError),
        ("Some/path", "/somes/path", WrongPathError),
        ("Some/path", "somes/path/", WrongPathError),
        ("Some/path", "/somes/path/", WrongPathError),
        ("Some/path", "some/paath", WrongPathError),
        ("Some/path", "/some/paath", WrongPathError),
        ("Some/path", "some/paath/", WrongPathError),
        ("Some/path", "/some/paath/", WrongPathError),
        ("Some/path", "x/some/path", WrongPathError),
        ("Some/path", "some/path/x", WrongPathError),
        ("Some/path", "x/some/path/x", WrongPathError),
        ("some/Path", "some/path", HTTPContext),
        ("some/Path", "/some/path", HTTPContext),
        ("some/Path", "some/path/", HTTPContext),
        ("some/Path", "/some/path/", HTTPContext),
        ("some/Path", "somes/path", WrongPathError),
        ("some/Path", "/somes/path", WrongPathError),
        ("some/Path", "somes/path/", WrongPathError),
        ("some/Path", "/somes/path/", WrongPathError),
        ("some/Path", "some/paath", WrongPathError),
        ("some/Path", "/some/paath", WrongPathError),
        ("some/Path", "some/paath/", WrongPathError),
        ("some/Path", "/some/paath/", WrongPathError),
        ("some/Path", "x/some/path", WrongPathError),
        ("some/Path", "some/path/x", WrongPathError),
        ("some/Path", "x/some/path/x", WrongPathError),
        ("path", "Path", HTTPContext),
        ("path", "/Path", HTTPContext),
        ("path", "Path/", HTTPContext),
        ("path", "/Path/", HTTPContext),
        ("path", "Paths", WrongPathError),
        ("path", "/Paths", WrongPathError),
        ("path", "Paths/", WrongPathError),
        ("path", "/Paths/", WrongPathError),
        ("some/path", "Some/path", HTTPContext),
        ("some/path", "/Some/path", HTTPContext),
        ("some/path", "Some/path/", HTTPContext),
        ("some/path", "/Some/path/", HTTPContext),
        ("some/path", "Somes/path", WrongPathError),
        ("some/path", "/Somes/path", WrongPathError),
        ("some/path", "Somes/path/", WrongPathError),
        ("some/path", "/Somes/path/", WrongPathError),
        ("some/path", "Some/paath", WrongPathError),
        ("some/path", "/Some/paath", WrongPathError),
        ("some/path", "Some/paath/", WrongPathError),
        ("some/path", "/Some/paath/", WrongPathError),
        ("some/path", "x/Some/path", WrongPathError),
        ("some/path", "Some/path/x", WrongPathError),
        ("some/path", "x/Some/path/x", WrongPathError),
    ],
)
def test_ci_route(ctx: HTTPContext, ctx_path, path, result_type):
    ctx.request.path = ctx_path
    assert isinstance(
        ctx >> ci_route(path),
        result_type,
    )


@pytest.mark.parametrize(
    "ctx_path, path, result_path, result_type",
    [
        ("subroute/path", "subroute", "path", HTTPContext),
        ("subroute/path", "subroute/", "path", HTTPContext),
        ("subroute/path", "/subroute", "path", HTTPContext),
        ("subroute/path", "/subroute/", "path", HTTPContext),
        ("subroute/path", "subroutes", "subroute/path", WrongPathError),
        ("subroute/path", "subroutes/", "subroute/path", WrongPathError),
        ("subroute/path", "/subroutes", "subroute/path", WrongPathError),
        ("subroute/path", "/subroutes/", "subroute/path", WrongPathError),
        ("Subroute/path", "subroute", "path", HTTPContext),
        ("Subroute/path", "subroute/", "path", HTTPContext),
        ("Subroute/path", "/subroute", "path", HTTPContext),
        ("Subroute/path", "/subroute/", "path", HTTPContext),
        ("Subroute/path", "subroutes", "subroute/path", WrongPathError),
        ("Subroute/path", "subroutes/", "subroute/path", WrongPathError),
        ("Subroute/path", "/subroutes", "subroute/path", WrongPathError),
        ("Subroute/path", "/subroutes/", "subroute/path", WrongPathError),
        ("subroute/Path", "subroute", "Path", HTTPContext),
        ("subroute/Path", "subroute/", "Path", HTTPContext),
        ("subroute/Path", "/subroute", "Path", HTTPContext),
        ("subroute/Path", "/subroute/", "Path", HTTPContext),
        ("subroute/Path", "subroutes", "subroute/Path", WrongPathError),
        ("subroute/Path", "subroutes/", "subroute/Path", WrongPathError),
        ("subroute/Path", "/subroutes", "subroute/Path", WrongPathError),
        ("subroute/Path", "/subroutes/", "subroute/Path", WrongPathError),
        ("subroute/path", "subroute", "path", HTTPContext),
        ("subroute/path", "suBroute/", "path", HTTPContext),
        ("subroute/path", "/suBroute", "path", HTTPContext),
        ("subroute/path", "/suBroute/", "path", HTTPContext),
        ("subroute/path", "suBroutes", "subroute/path", WrongPathError),
        ("subroute/path", "suBroutes/", "subroute/path", WrongPathError),
        ("subroute/path", "/suBroutes", "subroute/path", WrongPathError),
        ("subroute/path", "/suBroutes/", "subroute/path", WrongPathError),
    ],
)
def test_ci_subroute(ctx: HTTPContext, ctx_path, path, result_path, result_type):
    ctx.request.path = ctx_path
    result = ctx >> ci_subroute(path)
    match result:
        case HTTPContext():
            assert result.request.path == result_path
        case WrongPathError():
            assert isinstance(result, result_type)
