from dataclasses import dataclass

from mona.monads.result import Failure, Result, Success


@dataclass
class User:
    id: int
    name: str
    age: int
    role: str


__users = {
    1: User(1, "John", 21, "admin"),
    2: User(2, "Maria", 40, "modetator"),
    3: User(3, "Ivan", 28, "user"),
    4: User(4, "Alex", 13, "user"),
    5: User(5, "Nicole", 19, "user"),
}


def get_user(id: int) -> Result[User, Exception]:
    match __users.get(id, None):
        case User() as user:
            return Success(user)
        case None:
            return Failure(Exception(f"No user with id: {id}"))


def user_is_moderator(user: User) -> Result[User, Exception]:
    match user:
        case User(role="modetator") as user:
            return Success(user)
        case _:
            return Failure(Exception(f"User {user.name} is not moderator!"))


def make_user_admin(user: User) -> Success[User]:
    user.role = "admin"
    return Success(user)


def update_user(user: User) -> Result[User, Exception]:
    match __users.get(user.id, None):
        case None:
            return Failure(Exception("Can't update user with id {user.id}"))
        case _:
            __users[user.id] = user
            return Success(user)


# this is complete declarative railroad use-case
def make_moderator_admin(id: int) -> Result[User, Exception]:
    # Result also overrides >> for function binding
    return get_user(id) >> user_is_moderator >> make_user_admin >> update_user


result = make_moderator_admin(1)
print(result)  # Failure(value=Exception('User John is not moderator!'))


result = make_moderator_admin(2)
print(result)  # Success(value=User(id=2, name='Maria', age=40, role='admin'))
print(__users[2])  # User(id=2, name='Maria', age=40, role='admin')

# can be run as-is
