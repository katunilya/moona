import pytest

from mona import context, req, state


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state",
    [
        ("path", "path", state.RIGHT, state.RIGHT),
        ("path", "/path", state.RIGHT, state.RIGHT),
        ("path", "path/", state.RIGHT, state.RIGHT),
        ("path", "/path/", state.RIGHT, state.RIGHT),
        ("path", "paths", state.RIGHT, state.WRONG),
        ("path", "/paths", state.RIGHT, state.WRONG),
        ("path", "paths/", state.RIGHT, state.WRONG),
        ("path", "/paths/", state.RIGHT, state.WRONG),
        ("some/path", "some/path", state.RIGHT, state.RIGHT),
        ("some/path", "/some/path", state.RIGHT, state.RIGHT),
        ("some/path", "some/path/", state.RIGHT, state.RIGHT),
        ("some/path", "/some/path/", state.RIGHT, state.RIGHT),
        ("some/path", "somes/path", state.RIGHT, state.WRONG),
        ("some/path", "/somes/path", state.RIGHT, state.WRONG),
        ("some/path", "somes/path/", state.RIGHT, state.WRONG),
        ("some/path", "/somes/path/", state.RIGHT, state.WRONG),
        ("some/path", "some/paath", state.RIGHT, state.WRONG),
        ("some/path", "/some/paath", state.RIGHT, state.WRONG),
        ("some/path", "some/paath/", state.RIGHT, state.WRONG),
        ("some/path", "/some/paath/", state.RIGHT, state.WRONG),
        ("some/path", "x/some/path", state.RIGHT, state.WRONG),
        ("some/path", "some/path/x", state.RIGHT, state.WRONG),
        ("some/path", "x/some/path/x", state.RIGHT, state.WRONG),
        ("path", "path", state.WRONG, state.WRONG),
        ("path", "/path", state.WRONG, state.WRONG),
        ("path", "path/", state.WRONG, state.WRONG),
        ("path", "/path/", state.WRONG, state.WRONG),
        ("path", "paths", state.WRONG, state.WRONG),
        ("path", "/paths", state.WRONG, state.WRONG),
        ("path", "paths/", state.WRONG, state.WRONG),
        ("path", "/paths/", state.WRONG, state.WRONG),
        ("some/path", "some/path", state.WRONG, state.WRONG),
        ("some/path", "/some/path", state.WRONG, state.WRONG),
        ("some/path", "some/path/", state.WRONG, state.WRONG),
        ("some/path", "/some/path/", state.WRONG, state.WRONG),
        ("some/path", "somes/path", state.WRONG, state.WRONG),
        ("some/path", "/somes/path", state.WRONG, state.WRONG),
        ("some/path", "somes/path/", state.WRONG, state.WRONG),
        ("some/path", "/somes/path/", state.WRONG, state.WRONG),
        ("some/path", "some/paath", state.WRONG, state.WRONG),
        ("some/path", "/some/paath", state.WRONG, state.WRONG),
        ("some/path", "some/paath/", state.WRONG, state.WRONG),
        ("some/path", "/some/paath/", state.WRONG, state.WRONG),
        ("some/path", "x/some/path", state.WRONG, state.WRONG),
        ("some/path", "some/path/x", state.WRONG, state.WRONG),
        ("some/path", "x/some/path/x", state.WRONG, state.WRONG),
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
    ctx = state.pack(arrange_state, mock_context)
    handler = req.on_route(arrange_pattern)

    # act
    ctx: context.StateContext = handler(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state",
    [
        ("path", "path", state.RIGHT, state.RIGHT),
        ("path", "/path", state.RIGHT, state.RIGHT),
        ("path", "path/", state.RIGHT, state.RIGHT),
        ("path", "/path/", state.RIGHT, state.RIGHT),
        ("path", "paths", state.RIGHT, state.WRONG),
        ("path", "/paths", state.RIGHT, state.WRONG),
        ("path", "paths/", state.RIGHT, state.WRONG),
        ("path", "/paths/", state.RIGHT, state.WRONG),
        ("some/path", "some/path", state.RIGHT, state.RIGHT),
        ("some/path", "/some/path", state.RIGHT, state.RIGHT),
        ("some/path", "some/path/", state.RIGHT, state.RIGHT),
        ("some/path", "/some/path/", state.RIGHT, state.RIGHT),
        ("some/path", "somes/path", state.RIGHT, state.WRONG),
        ("some/path", "/somes/path", state.RIGHT, state.WRONG),
        ("some/path", "somes/path/", state.RIGHT, state.WRONG),
        ("some/path", "/somes/path/", state.RIGHT, state.WRONG),
        ("some/path", "some/paath", state.RIGHT, state.WRONG),
        ("some/path", "/some/paath", state.RIGHT, state.WRONG),
        ("some/path", "some/paath/", state.RIGHT, state.WRONG),
        ("some/path", "/some/paath/", state.RIGHT, state.WRONG),
        ("some/path", "x/some/path", state.RIGHT, state.WRONG),
        ("some/path", "some/path/x", state.RIGHT, state.WRONG),
        ("some/path", "x/some/path/x", state.RIGHT, state.WRONG),
        ("Path", "path", state.RIGHT, state.RIGHT),
        ("Path", "/path", state.RIGHT, state.RIGHT),
        ("Path", "path/", state.RIGHT, state.RIGHT),
        ("Path", "/path/", state.RIGHT, state.RIGHT),
        ("Path", "paths", state.RIGHT, state.WRONG),
        ("Path", "/paths", state.RIGHT, state.WRONG),
        ("Path", "paths/", state.RIGHT, state.WRONG),
        ("Path", "/paths/", state.RIGHT, state.WRONG),
        ("sOme/path", "some/path", state.RIGHT, state.RIGHT),
        ("sOme/path", "/some/path", state.RIGHT, state.RIGHT),
        ("sOme/path", "some/path/", state.RIGHT, state.RIGHT),
        ("sOme/path", "/some/path/", state.RIGHT, state.RIGHT),
        ("sOme/path", "somes/path", state.RIGHT, state.WRONG),
        ("sOme/path", "/somes/path", state.RIGHT, state.WRONG),
        ("sOme/path", "somes/path/", state.RIGHT, state.WRONG),
        ("sOme/path", "/somes/path/", state.RIGHT, state.WRONG),
        ("sOme/path", "some/paath", state.RIGHT, state.WRONG),
        ("sOme/path", "/some/paath", state.RIGHT, state.WRONG),
        ("sOme/path", "some/paath/", state.RIGHT, state.WRONG),
        ("sOme/path", "/some/paath/", state.RIGHT, state.WRONG),
        ("sOme/path", "x/some/path", state.RIGHT, state.WRONG),
        ("sOme/path", "some/path/x", state.RIGHT, state.WRONG),
        ("sOme/path", "x/some/path/x", state.RIGHT, state.WRONG),
        ("Path", "/pAth", state.RIGHT, state.RIGHT),
        ("Path", "pAth/", state.RIGHT, state.RIGHT),
        ("Path", "/pAth/", state.RIGHT, state.RIGHT),
        ("Path", "pAths", state.RIGHT, state.WRONG),
        ("Path", "/pAths", state.RIGHT, state.WRONG),
        ("Path", "pAths/", state.RIGHT, state.WRONG),
        ("Path", "/pAths/", state.RIGHT, state.WRONG),
        ("sOme/path", "some/patH", state.RIGHT, state.RIGHT),
        ("sOme/path", "/some/patH", state.RIGHT, state.RIGHT),
        ("sOme/path", "some/patH/", state.RIGHT, state.RIGHT),
        ("sOme/path", "/some/patH/", state.RIGHT, state.RIGHT),
        ("sOme/path", "somes/patH", state.RIGHT, state.WRONG),
        ("sOme/path", "/somes/patH", state.RIGHT, state.WRONG),
        ("sOme/path", "somes/patH/", state.RIGHT, state.WRONG),
        ("sOme/path", "/somes/patH/", state.RIGHT, state.WRONG),
        ("sOme/path", "some/paatH", state.RIGHT, state.WRONG),
        ("sOme/path", "/some/paatH", state.RIGHT, state.WRONG),
        ("sOme/path", "some/paatH/", state.RIGHT, state.WRONG),
        ("sOme/path", "/some/paatH/", state.RIGHT, state.WRONG),
        ("sOme/path", "x/some/patH", state.RIGHT, state.WRONG),
        ("sOme/path", "some/patH/x", state.RIGHT, state.WRONG),
        ("sOme/path", "x/some/patH/x", state.RIGHT, state.WRONG),
        ("path", "path", state.WRONG, state.WRONG),
        ("path", "/path", state.WRONG, state.WRONG),
        ("path", "path/", state.WRONG, state.WRONG),
        ("path", "/path/", state.WRONG, state.WRONG),
        ("path", "paths", state.WRONG, state.WRONG),
        ("path", "/paths", state.WRONG, state.WRONG),
        ("path", "paths/", state.WRONG, state.WRONG),
        ("path", "/paths/", state.WRONG, state.WRONG),
        ("some/path", "some/path", state.WRONG, state.WRONG),
        ("some/path", "/some/path", state.WRONG, state.WRONG),
        ("some/path", "some/path/", state.WRONG, state.WRONG),
        ("some/path", "/some/path/", state.WRONG, state.WRONG),
        ("some/path", "somes/path", state.WRONG, state.WRONG),
        ("some/path", "/somes/path", state.WRONG, state.WRONG),
        ("some/path", "somes/path/", state.WRONG, state.WRONG),
        ("some/path", "/somes/path/", state.WRONG, state.WRONG),
        ("some/path", "some/paath", state.WRONG, state.WRONG),
        ("some/path", "/some/paath", state.WRONG, state.WRONG),
        ("some/path", "some/paath/", state.WRONG, state.WRONG),
        ("some/path", "/some/paath/", state.WRONG, state.WRONG),
        ("some/path", "x/some/path", state.WRONG, state.WRONG),
        ("some/path", "some/path/x", state.WRONG, state.WRONG),
        ("some/path", "x/some/path/x", state.WRONG, state.WRONG),
        ("Path", "path", state.WRONG, state.WRONG),
        ("Path", "/path", state.WRONG, state.WRONG),
        ("Path", "path/", state.WRONG, state.WRONG),
        ("Path", "/path/", state.WRONG, state.WRONG),
        ("Path", "paths", state.WRONG, state.WRONG),
        ("Path", "/paths", state.WRONG, state.WRONG),
        ("Path", "paths/", state.WRONG, state.WRONG),
        ("Path", "/paths/", state.WRONG, state.WRONG),
        ("sOme/path", "some/path", state.WRONG, state.WRONG),
        ("sOme/path", "/some/path", state.WRONG, state.WRONG),
        ("sOme/path", "some/path/", state.WRONG, state.WRONG),
        ("sOme/path", "/some/path/", state.WRONG, state.WRONG),
        ("sOme/path", "somes/path", state.WRONG, state.WRONG),
        ("sOme/path", "/somes/path", state.WRONG, state.WRONG),
        ("sOme/path", "somes/path/", state.WRONG, state.WRONG),
        ("sOme/path", "/somes/path/", state.WRONG, state.WRONG),
        ("sOme/path", "some/paath", state.WRONG, state.WRONG),
        ("sOme/path", "/some/paath", state.WRONG, state.WRONG),
        ("sOme/path", "some/paath/", state.WRONG, state.WRONG),
        ("sOme/path", "/some/paath/", state.WRONG, state.WRONG),
        ("sOme/path", "x/some/path", state.WRONG, state.WRONG),
        ("sOme/path", "some/path/x", state.WRONG, state.WRONG),
        ("sOme/path", "x/some/path/x", state.WRONG, state.WRONG),
        ("Path", "/pAth", state.WRONG, state.WRONG),
        ("Path", "pAth/", state.WRONG, state.WRONG),
        ("Path", "/pAth/", state.WRONG, state.WRONG),
        ("Path", "pAths", state.WRONG, state.WRONG),
        ("Path", "/pAths", state.WRONG, state.WRONG),
        ("Path", "pAths/", state.WRONG, state.WRONG),
        ("Path", "/pAths/", state.WRONG, state.WRONG),
        ("sOme/path", "some/patH", state.WRONG, state.WRONG),
        ("sOme/path", "/some/patH", state.WRONG, state.WRONG),
        ("sOme/path", "some/patH/", state.WRONG, state.WRONG),
        ("sOme/path", "/some/patH/", state.WRONG, state.WRONG),
        ("sOme/path", "somes/patH", state.WRONG, state.WRONG),
        ("sOme/path", "/somes/patH", state.WRONG, state.WRONG),
        ("sOme/path", "somes/patH/", state.WRONG, state.WRONG),
        ("sOme/path", "/somes/patH/", state.WRONG, state.WRONG),
        ("sOme/path", "some/paatH", state.WRONG, state.WRONG),
        ("sOme/path", "/some/paatH", state.WRONG, state.WRONG),
        ("sOme/path", "some/paatH/", state.WRONG, state.WRONG),
        ("sOme/path", "/some/paatH/", state.WRONG, state.WRONG),
        ("sOme/path", "x/some/patH", state.WRONG, state.WRONG),
        ("sOme/path", "some/patH/x", state.WRONG, state.WRONG),
        ("sOme/path", "x/some/patH/x", state.WRONG, state.WRONG),
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
    ctx = state.pack(arrange_state, mock_context)
    handler = req.on_ciroute(arrange_pattern)

    # act
    ctx: context.StateContext = handler(ctx)

    # assert
    assert ctx.state == assert_state


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state,arrange_afterpath",
    [
        ("subroute/path", "subroute", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "subroute/", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "/subroute", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "/subroute/", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "subroutes", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes/", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes/", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "subroute", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroute/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroute", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroute/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes/", state.WRONG, state.WRONG, "subroute/path"),
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
    ctx = state.pack(arrange_state, mock_context)
    handle = req.on_subroute(arrange_pattern)

    # act
    ctx: context.StateContext = handle(ctx)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.request.path == arrange_afterpath


@pytest.mark.parametrize(
    "arrange_path,arrange_pattern,arrange_state,assert_state,arrange_afterpath",
    [
        ("subroute/path", "subroute", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "subroute/", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "/subroute", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "/subroute/", state.RIGHT, state.RIGHT, "path"),
        ("subroute/path", "subroutes", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes/", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes", state.RIGHT, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes/", state.RIGHT, state.WRONG, "subroute/path"),
        ("Subroute/path", "subroute", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "subroute/", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "/subroute", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "/subroute/", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "subroutes", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "subroutes/", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroutes", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroutes/", state.RIGHT, state.WRONG, "Subroute/path"),
        ("subroute/path", "/subroutes/", state.RIGHT, state.WRONG, "subroute/path"),
        ("Subroute/path", "suBroute", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "suBroute/", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "/suBroute", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "/suBroute/", state.RIGHT, state.RIGHT, "path"),
        ("Subroute/path", "suBroutes", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "suBroutes/", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroutes", state.RIGHT, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroutes/", state.RIGHT, state.WRONG, "Subroute/path"),
        ("subroute/path", "subroute", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroute/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroute", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroute/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "subroutes/", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes", state.WRONG, state.WRONG, "subroute/path"),
        ("subroute/path", "/subroutes/", state.WRONG, state.WRONG, "subroute/path"),
        ("Subroute/path", "subroute", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "subroute/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroute", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroute/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "subroutes", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "subroutes/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroutes", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/subroutes/", state.WRONG, state.WRONG, "Subroute/path"),
        ("subroute/path", "/subroutes/", state.WRONG, state.WRONG, "subroute/path"),
        ("Subroute/path", "suBroute", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "suBroute/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroute", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroute/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "suBroutes", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "suBroutes/", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroutes", state.WRONG, state.WRONG, "Subroute/path"),
        ("Subroute/path", "/suBroutes/", state.WRONG, state.WRONG, "Subroute/path"),
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
    ctx = state.pack(arrange_state, mock_context)
    handle = req.on_cisubroute(arrange_pattern)

    # act
    ctx: context.StateContext = handle(ctx)

    # assert
    assert ctx.state == assert_state
    assert ctx.value.request.path == arrange_afterpath
