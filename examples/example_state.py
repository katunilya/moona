import dataclasses

from mona import state


@dataclasses.dataclass
class User:  # noqa
    name: str
    age: int
    role: str


__users = [
    User("John", 21, "admin"),
    User("Maria", 40, "modetator"),
    User("Ivan", 28, "user"),
    User("Alex", 13, "user"),
    User("Nicole", 19, "user"),
]


def get_admin(name: str) -> state.ESafe[User]:  # noqa
    match next((u for u in __users if u.name == name), None):
        case User(role="admin") as user:
            return state.Right(user)
        case _:
            return state.Error(Exception(f"User {name} is not admin!"))


print(get_admin("John"))
print(get_admin("Ivan"))
