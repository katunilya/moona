from mona import context, res


def test_response_set_status(asgi_context: context.Context):
    _status = 201
    handler = res.set_status(_status)

    asgi_context = handler(asgi_context)

    assert asgi_context.response_status == _status
