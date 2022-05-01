import pytest

from mona.core import HTTPContext
from mona.handlers.route import ci_route, ci_subroute, route, subroute
from mona.monads.result import Failure, Result, Success


@pytest.mark.parametrize(
    "ctx_path, path, result_type",
    [
        ("path", "path", Success),
        ("path", "/path", Success),
        ("path", "path/", Success),
        ("path", "/path/", Success),
        ("path", "paths", Failure),
        ("path", "/paths", Failure),
        ("path", "paths/", Failure),
        ("path", "/paths/", Failure),
        ("some/path", "some/path", Success),
        ("some/path", "/some/path", Success),
        ("some/path", "some/path/", Success),
        ("some/path", "/some/path/", Success),
        ("some/path", "somes/path", Failure),
        ("some/path", "/somes/path", Failure),
        ("some/path", "somes/path/", Failure),
        ("some/path", "/somes/path/", Failure),
        ("some/path", "some/paath", Failure),
        ("some/path", "/some/paath", Failure),
        ("some/path", "some/paath/", Failure),
        ("some/path", "/some/paath/", Failure),
        ("some/path", "x/some/path", Failure),
        ("some/path", "some/path/x", Failure),
        ("some/path", "x/some/path/x", Failure),
    ],
)
def test_route(ctx: HTTPContext, ctx_path, path, result_type):
    ctx.request.path = ctx_path
    assert isinstance(
        route(path)(Result.successfull(ctx)),
        result_type,
    )


@pytest.mark.parametrize(
    "ctx_path, path, result_path, result_type",
    [
        ("subroute/path", "subroute", "path", Success),
        ("subroute/path", "subroute/", "path", Success),
        ("subroute/path", "/subroute", "path", Success),
        ("subroute/path", "/subroute/", "path", Success),
        ("subroute/path", "subroutes", "subroute/path", Failure),
        ("subroute/path", "subroutes/", "subroute/path", Failure),
        ("subroute/path", "/subroutes", "subroute/path", Failure),
        ("subroute/path", "/subroutes/", "subroute/path", Failure),
    ],
)
def test_subroute(ctx: HTTPContext, ctx_path, path, result_path, result_type):
    ctx.request.path = ctx_path
    result = subroute(path)(Result.successfull(ctx))
    match result:
        case Success():
            assert result.value.request.path == result_path
        case Failure():
            assert isinstance(result, result_type)


@pytest.mark.parametrize(
    "ctx_path, path, result_type",
    [
        ("path", "path", Success),
        ("path", "/path", Success),
        ("path", "path/", Success),
        ("path", "/path/", Success),
        ("path", "paths", Failure),
        ("path", "/paths", Failure),
        ("path", "paths/", Failure),
        ("path", "/paths/", Failure),
        ("some/path", "some/path", Success),
        ("some/path", "/some/path", Success),
        ("some/path", "some/path/", Success),
        ("some/path", "/some/path/", Success),
        ("some/path", "somes/path", Failure),
        ("some/path", "/somes/path", Failure),
        ("some/path", "somes/path/", Failure),
        ("some/path", "/somes/path/", Failure),
        ("some/path", "some/paath", Failure),
        ("some/path", "/some/paath", Failure),
        ("some/path", "some/paath/", Failure),
        ("some/path", "/some/paath/", Failure),
        ("some/path", "x/some/path", Failure),
        ("some/path", "some/path/x", Failure),
        ("some/path", "x/some/path/x", Failure),
        ("Path", "path", Success),
        ("Path", "/path", Success),
        ("Path", "path/", Success),
        ("Path", "/path/", Success),
        ("Path", "paths", Failure),
        ("Path", "/paths", Failure),
        ("Path", "paths/", Failure),
        ("Path", "/paths/", Failure),
        ("Some/path", "some/path", Success),
        ("Some/path", "/some/path", Success),
        ("Some/path", "some/path/", Success),
        ("Some/path", "/some/path/", Success),
        ("Some/path", "somes/path", Failure),
        ("Some/path", "/somes/path", Failure),
        ("Some/path", "somes/path/", Failure),
        ("Some/path", "/somes/path/", Failure),
        ("Some/path", "some/paath", Failure),
        ("Some/path", "/some/paath", Failure),
        ("Some/path", "some/paath/", Failure),
        ("Some/path", "/some/paath/", Failure),
        ("Some/path", "x/some/path", Failure),
        ("Some/path", "some/path/x", Failure),
        ("Some/path", "x/some/path/x", Failure),
        ("some/Path", "some/path", Success),
        ("some/Path", "/some/path", Success),
        ("some/Path", "some/path/", Success),
        ("some/Path", "/some/path/", Success),
        ("some/Path", "somes/path", Failure),
        ("some/Path", "/somes/path", Failure),
        ("some/Path", "somes/path/", Failure),
        ("some/Path", "/somes/path/", Failure),
        ("some/Path", "some/paath", Failure),
        ("some/Path", "/some/paath", Failure),
        ("some/Path", "some/paath/", Failure),
        ("some/Path", "/some/paath/", Failure),
        ("some/Path", "x/some/path", Failure),
        ("some/Path", "some/path/x", Failure),
        ("some/Path", "x/some/path/x", Failure),
        ("path", "Path", Success),
        ("path", "/Path", Success),
        ("path", "Path/", Success),
        ("path", "/Path/", Success),
        ("path", "Paths", Failure),
        ("path", "/Paths", Failure),
        ("path", "Paths/", Failure),
        ("path", "/Paths/", Failure),
        ("some/path", "Some/path", Success),
        ("some/path", "/Some/path", Success),
        ("some/path", "Some/path/", Success),
        ("some/path", "/Some/path/", Success),
        ("some/path", "Somes/path", Failure),
        ("some/path", "/Somes/path", Failure),
        ("some/path", "Somes/path/", Failure),
        ("some/path", "/Somes/path/", Failure),
        ("some/path", "Some/paath", Failure),
        ("some/path", "/Some/paath", Failure),
        ("some/path", "Some/paath/", Failure),
        ("some/path", "/Some/paath/", Failure),
        ("some/path", "x/Some/path", Failure),
        ("some/path", "Some/path/x", Failure),
        ("some/path", "x/Some/path/x", Failure),
    ],
)
def test_ci_route(ctx: HTTPContext, ctx_path, path, result_type):
    ctx.request.path = ctx_path
    assert isinstance(
        ci_route(path)(Result.successfull(ctx)),
        result_type,
    )


@pytest.mark.parametrize(
    "ctx_path, path, result_path, result_type",
    [
        ("subroute/path", "subroute", "path", Success),
        ("subroute/path", "subroute/", "path", Success),
        ("subroute/path", "/subroute", "path", Success),
        ("subroute/path", "/subroute/", "path", Success),
        ("subroute/path", "subroutes", "subroute/path", Failure),
        ("subroute/path", "subroutes/", "subroute/path", Failure),
        ("subroute/path", "/subroutes", "subroute/path", Failure),
        ("subroute/path", "/subroutes/", "subroute/path", Failure),
        ("Subroute/path", "subroute", "path", Success),
        ("Subroute/path", "subroute/", "path", Success),
        ("Subroute/path", "/subroute", "path", Success),
        ("Subroute/path", "/subroute/", "path", Success),
        ("Subroute/path", "subroutes", "subroute/path", Failure),
        ("Subroute/path", "subroutes/", "subroute/path", Failure),
        ("Subroute/path", "/subroutes", "subroute/path", Failure),
        ("Subroute/path", "/subroutes/", "subroute/path", Failure),
        ("subroute/Path", "subroute", "Path", Success),
        ("subroute/Path", "subroute/", "Path", Success),
        ("subroute/Path", "/subroute", "Path", Success),
        ("subroute/Path", "/subroute/", "Path", Success),
        ("subroute/Path", "subroutes", "subroute/Path", Failure),
        ("subroute/Path", "subroutes/", "subroute/Path", Failure),
        ("subroute/Path", "/subroutes", "subroute/Path", Failure),
        ("subroute/Path", "/subroutes/", "subroute/Path", Failure),
        ("subroute/path", "subroute", "path", Success),
        ("subroute/path", "suBroute/", "path", Success),
        ("subroute/path", "/suBroute", "path", Success),
        ("subroute/path", "/suBroute/", "path", Success),
        ("subroute/path", "suBroutes", "subroute/path", Failure),
        ("subroute/path", "suBroutes/", "subroute/path", Failure),
        ("subroute/path", "/suBroutes", "subroute/path", Failure),
        ("subroute/path", "/suBroutes/", "subroute/path", Failure),
    ],
)
def test_ci_subroute(ctx: HTTPContext, ctx_path, path, result_path, result_type):
    ctx.request.path = ctx_path
    result = ci_subroute(path)(Result.successfull(ctx))
    match result:
        case Success():
            assert result.value.request.path == result_path
        case Failure():
            assert isinstance(result, result_type)
