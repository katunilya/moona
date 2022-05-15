from typing import Any, Callable

from moona.monads.maybe import Maybe, Nothing, Some


def get_key(key: Any) -> Callable[[dict], Maybe]:
    def _get_key(dct: dict) -> Maybe:
        match dct.get(key, None):
            case None:
                return Nothing()
            case some:
                return Some(some)

    return _get_key


john_doe = {
    "id": 234,
    "name": "John Doe",
    "info": {
        "articles": [23, 2345, 3334],
        "friends": [233, 245, 265],
        "emails": {
            "main": "john_doe@example.org",
            "additional": "john_doe@recovery.org",
        },
    },
}

mary_jane = {
    "id": 33,
    "name": "Mary Jane",
    "info": {
        "articles": [10, 2345],
        "emails": {
            "main": "john_doe@example.org",
        },
    },
}


def get_addition_user_email(user: dict) -> Maybe[str]:
    return Some(user) >> get_key("info") >> get_key("emails") >> get_key("additional")


def get_user_friends(user: dict) -> Maybe[list[int]]:
    match Some(user) >> get_key("info") >> get_key("friends"):
        case Nothing():
            return Nothing()
        case Some([]):
            return Nothing()
        case friends:
            return friends


maybe = get_addition_user_email(john_doe)
print(maybe)  # Some(value='john_doe@recovery.org')

maybe = get_user_friends(john_doe)
print(maybe)  # Some(value=[233, 245, 265])

maybe = get_addition_user_email(mary_jane)
print(maybe)  # Nothing(value=None, _Nothing__instance=...)

maybe = get_user_friends(mary_jane)
print(maybe)  # Nothing(value=None, _Nothing__instance=...)
