from typing import Callable, Protocol


class Bindable(Protocol):
    """Interface for monad containers that support binding.

    Binding is application of passed function on some monad-specific pre-condition or
    action. Binding is done via `>>` operator. Commonly binding is applied only when
    container is in some "right" state and computation can be continued.
    """

    def __rshift__(self, func: Callable):
        """Dunder method for `func` binding.

        Args:
            func (Callable): function to bind
        """


class Alterable(Protocol):
    """Interface for monad containers that support altering.

    Altering is application of passed function on some monad-specific pre-condition or
    action. Altering is done via `<<` operator. Commonly altering is applied only when
    container is in some "wrong" state and computation cannot be continued. Opposite of
    binding.
    """

    def __lshift__(self, func: Callable):
        """Dunder method for `func` altering.

        Args:
            func (Callable): function to alter
        """
