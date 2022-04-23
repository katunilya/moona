from mona import asgi, req, res
from mona.monads import future

app = asgi.create(
    future.compose(
        req.on_http,
        res.set_body_text("Hello!"),
        res.send_start,
        res.send_body,
    )
)
