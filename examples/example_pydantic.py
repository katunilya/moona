from pydantic import BaseModel

from moona import asgi, http


class User(BaseModel):
    username: str
    name: str
    email: str
    age: int


user = User(username="jdoe", name="John Doe", email="john_doe@example.org", age=33)

app = asgi.create(http_handler=http.negotiate(user))
