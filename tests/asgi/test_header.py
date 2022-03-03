from mona import ASGIContext, header


def test_set(context: ASGIContext):

    key, value = "Content-Type", "text/plain"
    handler = header.set(key, value)

    context = handler(context)

    assert context.response_headers.get(key) == value
