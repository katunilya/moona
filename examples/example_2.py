from mona import asgi, handler, req, res
from mona.monads import future

index = future.compose(
    req.on_get,
    req.on_route("/"),
    res.set_body_text("Index Handler"),
    res.send_start,
    res.send_body,
)

hello_world = future.compose(
    req.on_get,
    req.on_route("/hello"),
    res.set_body_text("Hello, user!"),
    res.send_start,
    res.send_body,
)

not_found = future.compose(
    res.set_status_not_found,
    res.set_body_text("Not found"),
    res.send_start,
    res.send_body,
)

router = future.compose(
    req.on_http,
    handler.choose(
        index,
        hello_world,
        not_found,
    ),
)

app = asgi.create(router)
