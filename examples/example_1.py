from mona import asgi, future, req, res

app = asgi.create(
    future.compose(
        req.on_http,
        res.set_body_text("Hello!"),
        res.send_start,
        res.send_body,
    )
)
