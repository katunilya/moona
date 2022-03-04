import pytest
from mona import context, res


def test_response_set_body(asgi_context: context.Context):

    body_data = b"Hello World!"
    handler = res.set_body(body_data)

    asgi_context = handler(asgi_context)

    assert asgi_context.response_body == body_data


def test_response_set_body_text(asgi_context: context.Context):

    text = "Hello, World!"
    body_data = b"Hello, World!"

    handler = res.set_body_text(text)

    asgi_context = handler(asgi_context)

    assert asgi_context.response_body == body_data


@pytest.mark.asyncio
async def test_response_set_body_from_sync_function(asgi_context: context.Context):

    body_data = b"Hello, World!"

    def get_body(_):
        return body_data

    handler = res.set_body_from(get_body)

    asgi_context = await handler(asgi_context)

    assert asgi_context.response_body == body_data


@pytest.mark.asyncio
async def test_response_set_body_from_async_function(asgi_context: context.Context):

    body_data = b"Hello, World!"

    async def get_body(_):
        return body_data

    handler = res.set_body_from(get_body)

    asgi_context = await handler(asgi_context)

    assert asgi_context.response_body == body_data
