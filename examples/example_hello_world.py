import mona
from mona.handlers.body import send_body_text_async

# ASGI that return text/plain response 'Hello, World!!!" for any HTTP request
app = mona.create(
    send_body_text_async("Hello, World!!!"),
)
