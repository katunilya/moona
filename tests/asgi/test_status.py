from mona import ASGIContext, status


def test_status(context: ASGIContext):
    handler = status.set(status.CREATED)

    context = handler(context)

    assert context.response_status == status.CREATED
