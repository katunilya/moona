import pytest

from mona import context, req
from mona.monads import state


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state",
    [
        ("path", "path", state.Right, state.Right),
        ("path", "/path", state.Right, state.Right),
        ("path", "path/", state.Right, state.Right),
        ("path", "/path/", state.Right, state.Right),
        ("path", "paths", state.Right, state.Wrong),
        ("path", "/paths", state.Right, state.Wrong),
        ("path", "paths/", state.Right, state.Wrong),
        ("path", "/paths/", state.Right, state.Wrong),
        ("some/path", "some/path", state.Right, state.Right),
        ("some/path", "/some/path", state.Right, state.Right),
        ("some/path", "some/path/", state.Right, state.Right),
        ("some/path", "/some/path/", state.Right, state.Right),
        ("some/path", "somes/path", state.Right, state.Wrong),
        ("some/path", "/somes/path", state.Right, state.Wrong),
        ("some/path", "somes/path/", state.Right, state.Wrong),
        ("some/path", "/somes/path/", state.Right, state.Wrong),
        ("some/path", "some/paath", state.Right, state.Wrong),
        ("some/path", "/some/paath", state.Right, state.Wrong),
        ("some/path", "some/paath/", state.Right, state.Wrong),
        ("some/path", "/some/paath/", state.Right, state.Wrong),
        ("some/path", "x/some/path", state.Right, state.Wrong),
        ("some/path", "some/path/x", state.Right, state.Wrong),
        ("some/path", "x/some/path/x", state.Right, state.Wrong),
        ("path", "path", state.Wrong, state.Wrong),
        ("path", "/path", state.Wrong, state.Wrong),
        ("path", "path/", state.Wrong, state.Wrong),
        ("path", "/path/", state.Wrong, state.Wrong),
        ("path", "paths", state.Wrong, state.Wrong),
        ("path", "/paths", state.Wrong, state.Wrong),
        ("path", "paths/", state.Wrong, state.Wrong),
        ("path", "/paths/", state.Wrong, state.Wrong),
        ("some/path", "some/path", state.Wrong, state.Wrong),
        ("some/path", "/some/path", state.Wrong, state.Wrong),
        ("some/path", "some/path/", state.Wrong, state.Wrong),
        ("some/path", "/some/path/", state.Wrong, state.Wrong),
        ("some/path", "somes/path", state.Wrong, state.Wrong),
        ("some/path", "/somes/path", state.Wrong, state.Wrong),
        ("some/path", "somes/path/", state.Wrong, state.Wrong),
        ("some/path", "/somes/path/", state.Wrong, state.Wrong),
        ("some/path", "some/paath", state.Wrong, state.Wrong),
        ("some/path", "/some/paath", state.Wrong, state.Wrong),
        ("some/path", "some/paath/", state.Wrong, state.Wrong),
        ("some/path", "/some/paath/", state.Wrong, state.Wrong),
        ("some/path", "x/some/path", state.Wrong, state.Wrong),
        ("some/path", "some/path/x", state.Wrong, state.Wrong),
        ("some/path", "x/some/path/x", state.Wrong, state.Wrong),
    ],
)
def test_on_route(
    mock_context: context.Context,
    arrange_path,
    arrange_pattern,
    arrange_state,
    assert_state,
):
    # arrange
    mock_context.request.path = arrange_path.strip("/")
    arrange_ctx = arrange_state(mock_context)
    arrange_handler = req.on_route(arrange_pattern)

    # act
    act_ctx: context.StateContext = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state",
    [
        ("path", "path", state.Right, state.Right),
        ("path", "/path", state.Right, state.Right),
        ("path", "path/", state.Right, state.Right),
        ("path", "/path/", state.Right, state.Right),
        ("path", "paths", state.Right, state.Wrong),
        ("path", "/paths", state.Right, state.Wrong),
        ("path", "paths/", state.Right, state.Wrong),
        ("path", "/paths/", state.Right, state.Wrong),
        ("some/path", "some/path", state.Right, state.Right),
        ("some/path", "/some/path", state.Right, state.Right),
        ("some/path", "some/path/", state.Right, state.Right),
        ("some/path", "/some/path/", state.Right, state.Right),
        ("some/path", "somes/path", state.Right, state.Wrong),
        ("some/path", "/somes/path", state.Right, state.Wrong),
        ("some/path", "somes/path/", state.Right, state.Wrong),
        ("some/path", "/somes/path/", state.Right, state.Wrong),
        ("some/path", "some/paath", state.Right, state.Wrong),
        ("some/path", "/some/paath", state.Right, state.Wrong),
        ("some/path", "some/paath/", state.Right, state.Wrong),
        ("some/path", "/some/paath/", state.Right, state.Wrong),
        ("some/path", "x/some/path", state.Right, state.Wrong),
        ("some/path", "some/path/x", state.Right, state.Wrong),
        ("some/path", "x/some/path/x", state.Right, state.Wrong),
        ("Path", "path", state.Right, state.Right),
        ("Path", "/path", state.Right, state.Right),
        ("Path", "path/", state.Right, state.Right),
        ("Path", "/path/", state.Right, state.Right),
        ("Path", "paths", state.Right, state.Wrong),
        ("Path", "/paths", state.Right, state.Wrong),
        ("Path", "paths/", state.Right, state.Wrong),
        ("Path", "/paths/", state.Right, state.Wrong),
        ("sOme/path", "some/path", state.Right, state.Right),
        ("sOme/path", "/some/path", state.Right, state.Right),
        ("sOme/path", "some/path/", state.Right, state.Right),
        ("sOme/path", "/some/path/", state.Right, state.Right),
        ("sOme/path", "somes/path", state.Right, state.Wrong),
        ("sOme/path", "/somes/path", state.Right, state.Wrong),
        ("sOme/path", "somes/path/", state.Right, state.Wrong),
        ("sOme/path", "/somes/path/", state.Right, state.Wrong),
        ("sOme/path", "some/paath", state.Right, state.Wrong),
        ("sOme/path", "/some/paath", state.Right, state.Wrong),
        ("sOme/path", "some/paath/", state.Right, state.Wrong),
        ("sOme/path", "/some/paath/", state.Right, state.Wrong),
        ("sOme/path", "x/some/path", state.Right, state.Wrong),
        ("sOme/path", "some/path/x", state.Right, state.Wrong),
        ("sOme/path", "x/some/path/x", state.Right, state.Wrong),
        ("Path", "/pAth", state.Right, state.Right),
        ("Path", "pAth/", state.Right, state.Right),
        ("Path", "/pAth/", state.Right, state.Right),
        ("Path", "pAths", state.Right, state.Wrong),
        ("Path", "/pAths", state.Right, state.Wrong),
        ("Path", "pAths/", state.Right, state.Wrong),
        ("Path", "/pAths/", state.Right, state.Wrong),
        ("sOme/path", "some/patH", state.Right, state.Right),
        ("sOme/path", "/some/patH", state.Right, state.Right),
        ("sOme/path", "some/patH/", state.Right, state.Right),
        ("sOme/path", "/some/patH/", state.Right, state.Right),
        ("sOme/path", "somes/patH", state.Right, state.Wrong),
        ("sOme/path", "/somes/patH", state.Right, state.Wrong),
        ("sOme/path", "somes/patH/", state.Right, state.Wrong),
        ("sOme/path", "/somes/patH/", state.Right, state.Wrong),
        ("sOme/path", "some/paatH", state.Right, state.Wrong),
        ("sOme/path", "/some/paatH", state.Right, state.Wrong),
        ("sOme/path", "some/paatH/", state.Right, state.Wrong),
        ("sOme/path", "/some/paatH/", state.Right, state.Wrong),
        ("sOme/path", "x/some/patH", state.Right, state.Wrong),
        ("sOme/path", "some/patH/x", state.Right, state.Wrong),
        ("sOme/path", "x/some/patH/x", state.Right, state.Wrong),
        ("path", "path", state.Wrong, state.Wrong),
        ("path", "/path", state.Wrong, state.Wrong),
        ("path", "path/", state.Wrong, state.Wrong),
        ("path", "/path/", state.Wrong, state.Wrong),
        ("path", "paths", state.Wrong, state.Wrong),
        ("path", "/paths", state.Wrong, state.Wrong),
        ("path", "paths/", state.Wrong, state.Wrong),
        ("path", "/paths/", state.Wrong, state.Wrong),
        ("some/path", "some/path", state.Wrong, state.Wrong),
        ("some/path", "/some/path", state.Wrong, state.Wrong),
        ("some/path", "some/path/", state.Wrong, state.Wrong),
        ("some/path", "/some/path/", state.Wrong, state.Wrong),
        ("some/path", "somes/path", state.Wrong, state.Wrong),
        ("some/path", "/somes/path", state.Wrong, state.Wrong),
        ("some/path", "somes/path/", state.Wrong, state.Wrong),
        ("some/path", "/somes/path/", state.Wrong, state.Wrong),
        ("some/path", "some/paath", state.Wrong, state.Wrong),
        ("some/path", "/some/paath", state.Wrong, state.Wrong),
        ("some/path", "some/paath/", state.Wrong, state.Wrong),
        ("some/path", "/some/paath/", state.Wrong, state.Wrong),
        ("some/path", "x/some/path", state.Wrong, state.Wrong),
        ("some/path", "some/path/x", state.Wrong, state.Wrong),
        ("some/path", "x/some/path/x", state.Wrong, state.Wrong),
        ("Path", "path", state.Wrong, state.Wrong),
        ("Path", "/path", state.Wrong, state.Wrong),
        ("Path", "path/", state.Wrong, state.Wrong),
        ("Path", "/path/", state.Wrong, state.Wrong),
        ("Path", "paths", state.Wrong, state.Wrong),
        ("Path", "/paths", state.Wrong, state.Wrong),
        ("Path", "paths/", state.Wrong, state.Wrong),
        ("Path", "/paths/", state.Wrong, state.Wrong),
        ("sOme/path", "some/path", state.Wrong, state.Wrong),
        ("sOme/path", "/some/path", state.Wrong, state.Wrong),
        ("sOme/path", "some/path/", state.Wrong, state.Wrong),
        ("sOme/path", "/some/path/", state.Wrong, state.Wrong),
        ("sOme/path", "somes/path", state.Wrong, state.Wrong),
        ("sOme/path", "/somes/path", state.Wrong, state.Wrong),
        ("sOme/path", "somes/path/", state.Wrong, state.Wrong),
        ("sOme/path", "/somes/path/", state.Wrong, state.Wrong),
        ("sOme/path", "some/paath", state.Wrong, state.Wrong),
        ("sOme/path", "/some/paath", state.Wrong, state.Wrong),
        ("sOme/path", "some/paath/", state.Wrong, state.Wrong),
        ("sOme/path", "/some/paath/", state.Wrong, state.Wrong),
        ("sOme/path", "x/some/path", state.Wrong, state.Wrong),
        ("sOme/path", "some/path/x", state.Wrong, state.Wrong),
        ("sOme/path", "x/some/path/x", state.Wrong, state.Wrong),
        ("Path", "/pAth", state.Wrong, state.Wrong),
        ("Path", "pAth/", state.Wrong, state.Wrong),
        ("Path", "/pAth/", state.Wrong, state.Wrong),
        ("Path", "pAths", state.Wrong, state.Wrong),
        ("Path", "/pAths", state.Wrong, state.Wrong),
        ("Path", "pAths/", state.Wrong, state.Wrong),
        ("Path", "/pAths/", state.Wrong, state.Wrong),
        ("sOme/path", "some/patH", state.Wrong, state.Wrong),
        ("sOme/path", "/some/patH", state.Wrong, state.Wrong),
        ("sOme/path", "some/patH/", state.Wrong, state.Wrong),
        ("sOme/path", "/some/patH/", state.Wrong, state.Wrong),
        ("sOme/path", "somes/patH", state.Wrong, state.Wrong),
        ("sOme/path", "/somes/patH", state.Wrong, state.Wrong),
        ("sOme/path", "somes/patH/", state.Wrong, state.Wrong),
        ("sOme/path", "/somes/patH/", state.Wrong, state.Wrong),
        ("sOme/path", "some/paatH", state.Wrong, state.Wrong),
        ("sOme/path", "/some/paatH", state.Wrong, state.Wrong),
        ("sOme/path", "some/paatH/", state.Wrong, state.Wrong),
        ("sOme/path", "/some/paatH/", state.Wrong, state.Wrong),
        ("sOme/path", "x/some/patH", state.Wrong, state.Wrong),
        ("sOme/path", "some/patH/x", state.Wrong, state.Wrong),
        ("sOme/path", "x/some/patH/x", state.Wrong, state.Wrong),
    ],
)
def test_on_ciroute(
    mock_context: context.Context,
    arrange_path,
    arrange_pattern,
    arrange_state,
    assert_state,
):
    # arrange
    mock_context.request.path = arrange_path.strip("/")
    arrange_ctx = arrange_state(mock_context)
    arrange_handler = req.on_ciroute(arrange_pattern)

    # act
    act_ctx: context.StateContext = arrange_handler(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state,arrange_afterpath",
    [
        ("subroute/path", "subroute", state.Right, state.Right, "path"),
        ("subroute/path", "subroute/", state.Right, state.Right, "path"),
        ("subroute/path", "/subroute", state.Right, state.Right, "path"),
        ("subroute/path", "/subroute/", state.Right, state.Right, "path"),
        ("subroute/path", "subroutes", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes/", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes/", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "subroute", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroute/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroute", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroute/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes/", state.Wrong, state.Wrong, "subroute/path"),
    ],
)
def test_on_subroute(
    mock_context: context.Context,
    arrange_path,
    arrange_pattern,
    arrange_state,
    assert_state,
    arrange_afterpath,
):
    # arrange
    mock_context.request.path = arrange_path
    arrange_ctx = arrange_state(mock_context)
    arrange_handle = req.on_subroute(arrange_pattern)

    # act
    act_ctx: context.StateContext = arrange_handle(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.request.path == arrange_afterpath


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state,arrange_afterpath",
    [
        ("subroute/path", "subroute", state.Right, state.Right, "path"),
        ("subroute/path", "subroute/", state.Right, state.Right, "path"),
        ("subroute/path", "/subroute", state.Right, state.Right, "path"),
        ("subroute/path", "/subroute/", state.Right, state.Right, "path"),
        ("subroute/path", "subroutes", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes/", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes", state.Right, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes/", state.Right, state.Wrong, "subroute/path"),
        ("Subroute/path", "subroute", state.Right, state.Right, "path"),
        ("Subroute/path", "subroute/", state.Right, state.Right, "path"),
        ("Subroute/path", "/subroute", state.Right, state.Right, "path"),
        ("Subroute/path", "/subroute/", state.Right, state.Right, "path"),
        ("Subroute/path", "subroutes", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "subroutes/", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroutes", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroutes/", state.Right, state.Wrong, "Subroute/path"),
        ("subroute/path", "/subroutes/", state.Right, state.Wrong, "subroute/path"),
        ("Subroute/path", "suBroute", state.Right, state.Right, "path"),
        ("Subroute/path", "suBroute/", state.Right, state.Right, "path"),
        ("Subroute/path", "/suBroute", state.Right, state.Right, "path"),
        ("Subroute/path", "/suBroute/", state.Right, state.Right, "path"),
        ("Subroute/path", "suBroutes", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "suBroutes/", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroutes", state.Right, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroutes/", state.Right, state.Wrong, "Subroute/path"),
        ("subroute/path", "subroute", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroute/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroute", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroute/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "subroutes/", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes", state.Wrong, state.Wrong, "subroute/path"),
        ("subroute/path", "/subroutes/", state.Wrong, state.Wrong, "subroute/path"),
        ("Subroute/path", "subroute", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "subroute/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroute", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroute/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "subroutes", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "subroutes/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroutes", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/subroutes/", state.Wrong, state.Wrong, "Subroute/path"),
        ("subroute/path", "/subroutes/", state.Wrong, state.Wrong, "subroute/path"),
        ("Subroute/path", "suBroute", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "suBroute/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroute", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroute/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "suBroutes", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "suBroutes/", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroutes", state.Wrong, state.Wrong, "Subroute/path"),
        ("Subroute/path", "/suBroutes/", state.Wrong, state.Wrong, "Subroute/path"),
    ],
)
def test_on_cisubroute(
    mock_context: context.Context,
    arrange_path,
    arrange_pattern,
    arrange_state,
    assert_state,
    arrange_afterpath,
):
    # arrange
    mock_context.request.path = arrange_path
    arrange_ctx = arrange_state(mock_context)
    arrange_handle = req.on_cisubroute(arrange_pattern)

    # act
    act_ctx: context.StateContext = arrange_handle(arrange_ctx)

    # assert
    assert isinstance(act_ctx, assert_state)
    assert act_ctx.value.request.path == arrange_afterpath
