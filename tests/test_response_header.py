from mona import context, res


def test_response_set_header(asgi_context: context.Context):

    key, value = "Content-Type", "text/plain"
    handler = res.set_header(key, value)

    asgi_context = handler(asgi_context)

    assert asgi_context.response_headers.get(key) == value
