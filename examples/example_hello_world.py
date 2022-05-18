from moona import asgi, http

app = asgi.create(http_handler=http.text("Hello, World!!!"))
