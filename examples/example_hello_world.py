import moona
from moona import http
from moona.monads import Func

# ASGI that return text/plain response 'Hello, World!!!" for any HTTP request
app = moona.create(
    Func()
    .then(http.set_response_body_text("Hello World!!!"))
    .then_future(http.send_response_body_async)
)
