import pytest
from mona import ASGIContext, body


def test_set(context: ASGIContext):

    body_data = b"Hello World!"
    handler = body.set(body_data)

    context = handler(context)

    assert context.response_body == body_data


def test_set_text(context: ASGIContext):

    text = "Hello, World!"
    body_data = b"Hello, World!"

    handler = body.set_text(text)

    context = handler(context)

    assert context.response_body == body_data


@pytest.mark.asyncio
async def test_set_from_sync_function(context: ASGIContext):

    body_data = b"Hello, World!"

    def get_body(_):
        return body_data

    handler = body.set_from(get_body)

    context = await handler(context)

    assert context.response_body == body_data


@pytest.mark.asyncio
async def test_set_from_async_function(context: ASGIContext):

    body_data = b"Hello, World!"

    async def get_body(_):
        return body_data

    handler = body.set_from(get_body)

    context = await handler(context)

    assert context.response_body == body_data
