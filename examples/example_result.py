from dataclasses import dataclass

from mona.monads.result import Result


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


@Result.returns
def get_user(id: int) -> Result[User, Exception]:
    match __users.get(id, None):
        case User() as user:
            return user
        case None:
            return Exception(f"No user with id: {id}")


@Result.returns
def user_is_moderator(user: User) -> User | Exception:
    match user:
        case User(role="modetator") as user:
            return user
        case _:
            return Exception(f"User {user.name} is not moderator!")


@Result.returns
def make_user_admin(user: User) -> User:
    user.role = "admin"
    return user


@Result.returns
def update_user(user: User) -> User | Exception:
    match __users.get(user.id, None):
        case None:
            return Exception("Can't update user with id {user.id}")
        case _:
            __users[user.id] = user
            return user


# this is complete declarative railroad use-case
def make_moderator_admin(id: int) -> Result[User, Exception]:
    return get_user(id).then(user_is_moderator).then(make_user_admin).then(update_user)


result = make_moderator_admin(1)
print(result)  # Bad(value=Exception('User John is not moderator!'))


result = make_moderator_admin(2)
print(result)  # Ok(value=User(id=2, name='Maria', age=40, role='admin'))
print(__users[2])  # User(id=2, name='Maria', age=40, role='admin')

# can be run as-is
