from typing import Callable

import pytest

from moona.http.context import HTTPContext
from moona.http.handlers import HTTPHandler, end
from moona.http.request_route import bind_query, route, route_ci, subroute, subroute_ci


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx_path, path, result",
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
async def test_route(ctx: HTTPContext, ctx_path, path, result):
    ctx.request_path = ctx_path
    _ctx = await route(path)(end, ctx)
    assert (_ctx is not None) == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx_path, path, result_path, result",
    [
        ("subroute/path", "subroute", "path", True),
        ("subroute/path", "subroute/", "path", True),
        ("subroute/path", "/subroute", "path", True),
        ("subroute/path", "/subroute/", "path", True),
        ("subroute/path", "subroutes", "subroute/path", False),
        ("subroute/path", "subroutes/", "subroute/path", False),
        ("subroute/path", "/subroutes", "subroute/path", False),
        ("subroute/path", "/subroutes/", "subroute/path", False),
    ],
)
async def test_subroute(ctx: HTTPContext, ctx_path, path, result_path, result):
    ctx.request_path = ctx_path
    _ctx = await subroute(path)(end, ctx)
    assert (_ctx is not None) == result
    if _ctx:
        assert _ctx.request_path == result_path


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx_path, path, result",
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
        ("Some/path", "some/path", True),
        ("Some/path", "/some/path", True),
        ("Some/path", "some/path/", True),
        ("Some/path", "/some/path/", True),
        ("Some/path", "somes/path", False),
        ("Some/path", "/somes/path", False),
        ("Some/path", "somes/path/", False),
        ("Some/path", "/somes/path/", False),
        ("Some/path", "some/paath", False),
        ("Some/path", "/some/paath", False),
        ("Some/path", "some/paath/", False),
        ("Some/path", "/some/paath/", False),
        ("Some/path", "x/some/path", False),
        ("Some/path", "some/path/x", False),
        ("Some/path", "x/some/path/x", False),
        ("some/Path", "some/path", True),
        ("some/Path", "/some/path", True),
        ("some/Path", "some/path/", True),
        ("some/Path", "/some/path/", True),
        ("some/Path", "somes/path", False),
        ("some/Path", "/somes/path", False),
        ("some/Path", "somes/path/", False),
        ("some/Path", "/somes/path/", False),
        ("some/Path", "some/paath", False),
        ("some/Path", "/some/paath", False),
        ("some/Path", "some/paath/", False),
        ("some/Path", "/some/paath/", False),
        ("some/Path", "x/some/path", False),
        ("some/Path", "some/path/x", False),
        ("some/Path", "x/some/path/x", False),
        ("path", "Path", True),
        ("path", "/Path", True),
        ("path", "Path/", True),
        ("path", "/Path/", True),
        ("path", "Paths", False),
        ("path", "/Paths", False),
        ("path", "Paths/", False),
        ("path", "/Paths/", False),
        ("some/path", "Some/path", True),
        ("some/path", "/Some/path", True),
        ("some/path", "Some/path/", True),
        ("some/path", "/Some/path/", True),
        ("some/path", "Somes/path", False),
        ("some/path", "/Somes/path", False),
        ("some/path", "Somes/path/", False),
        ("some/path", "/Somes/path/", False),
        ("some/path", "Some/paath", False),
        ("some/path", "/Some/paath", False),
        ("some/path", "Some/paath/", False),
        ("some/path", "/Some/paath/", False),
        ("some/path", "x/Some/path", False),
        ("some/path", "Some/path/x", False),
        ("some/path", "x/Some/path/x", False),
    ],
)
async def test_ci_route(ctx: HTTPContext, ctx_path, path, result):
    ctx.request_path = ctx_path
    _ctx = await route_ci(path)(end, ctx)
    assert (_ctx is not None) == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx_path, path, result_path, result",
    [
        ("subroute/path", "subroute", "path", True),
        ("subroute/path", "subroute/", "path", True),
        ("subroute/path", "/subroute", "path", True),
        ("subroute/path", "/subroute/", "path", True),
        ("subroute/path", "subroutes", "subroute/path", False),
        ("subroute/path", "subroutes/", "subroute/path", False),
        ("subroute/path", "/subroutes", "subroute/path", False),
        ("subroute/path", "/subroutes/", "subroute/path", False),
        ("Subroute/path", "subroute", "path", True),
        ("Subroute/path", "subroute/", "path", True),
        ("Subroute/path", "/subroute", "path", True),
        ("Subroute/path", "/subroute/", "path", True),
        ("Subroute/path", "subroutes", "subroute/path", False),
        ("Subroute/path", "subroutes/", "subroute/path", False),
        ("Subroute/path", "/subroutes", "subroute/path", False),
        ("Subroute/path", "/subroutes/", "subroute/path", False),
        ("subroute/Path", "subroute", "Path", True),
        ("subroute/Path", "subroute/", "Path", True),
        ("subroute/Path", "/subroute", "Path", True),
        ("subroute/Path", "/subroute/", "Path", True),
        ("subroute/Path", "subroutes", "subroute/Path", False),
        ("subroute/Path", "subroutes/", "subroute/Path", False),
        ("subroute/Path", "/subroutes", "subroute/Path", False),
        ("subroute/Path", "/subroutes/", "subroute/Path", False),
        ("subroute/path", "subroute", "path", True),
        ("subroute/path", "suBroute/", "path", True),
        ("subroute/path", "/suBroute", "path", True),
        ("subroute/path", "/suBroute/", "path", True),
        ("subroute/path", "suBroutes", "subroute/path", False),
        ("subroute/path", "suBroutes/", "subroute/path", False),
        ("subroute/path", "/suBroutes", "subroute/path", False),
        ("subroute/path", "/suBroutes/", "subroute/path", False),
    ],
)
async def test_ci_subroute(ctx: HTTPContext, ctx_path, path, result_path, result):
    ctx.request_path = ctx_path
    _ctx = await subroute_ci(path)(end, ctx)
    assert (_ctx is not None) == result
    if _ctx:
        assert _ctx.request_path == result_path


def check_for(result) -> Callable[..., HTTPHandler]:
    def _check_for(**kwargs) -> HTTPHandler:
        assert kwargs == result
        return lambda _, ctx: end(ctx)

    return _check_for


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_string, handler",
    [
        (b"", check_for({})),
        (
            b"id=123&per_page=10&page=3",
            check_for({"id": "123", "per_page": "10", "page": "3"}),
        ),
    ],
)
async def test_bind_query(ctx: HTTPContext, query_string, handler):
    ctx.request_query_string = query_string
    await bind_query(handler)(end, ctx)
