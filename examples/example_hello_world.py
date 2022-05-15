from moona import asgi, http

app = asgi.create(http_handler=http.send_text("Hello, World!!!"))
