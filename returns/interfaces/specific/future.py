"""
Represents the base interfaces for types that do fearless async operations.

This type means that ``Future`` cannot fail.
Don't use this type for async that can. Instead, use
:class:`returns.interfaces.specific.future_result.FutureResultBasedN` type.
"""

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Generator,
    Generic,
    NoReturn,
    Type,
    TypeVar,
)

from returns.interfaces.specific import io
from returns.primitives.hkt import KindN

if TYPE_CHECKING:
    from returns.future import Future  # noqa: WPS433

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')

_FutureLikeType = TypeVar('_FutureLikeType', bound='FutureLikeN')
_AsyncFutureType = TypeVar('_AsyncFutureType', bound='AsyncFutureN')
_FutureBasedType = TypeVar('_FutureBasedType', bound='FutureBasedN')


class FutureLikeN(io.IOBasedN[_FirstType, _SecondType, _ThirdType]):
    """
    Base type for ones that does look like ``Future``.

    But at the time this is not a real ``Future`` and cannot be awaited.
    """

    @abstractmethod
    def bind_future(
        self: _FutureLikeType,
        function: Callable[[_FirstType], 'Future[_UpdatedType]'],
    ) -> KindN[_FutureLikeType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to apply a wrapped function over a container."""

    @abstractmethod  # TODO: add bind_async_future
    def bind_async(
        self: _FutureLikeType,
        function: Callable[
            [_FirstType],
            Awaitable[
                KindN[_FutureLikeType, _UpdatedType, _SecondType, _ThirdType],
            ],
        ],
    ) -> KindN[_FutureLikeType, _UpdatedType, _SecondType, _ThirdType]:
        """Binds async function returning the same type of container object."""

    @classmethod
    @abstractmethod
    def from_future(
        cls: Type[_FutureLikeType],  # noqa: N805
        inner_value: 'Future[_FirstType]',
    ) -> KindN[_FutureLikeType, _FirstType, _SecondType, _ThirdType]:
        """Unit method to create new containers from successful ``IO``."""


#: Type alias for kinds with one type argument.
FutureLike1 = FutureLikeN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
FutureLike2 = FutureLikeN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
FutureLike3 = FutureLikeN[_FirstType, _SecondType, _ThirdType]


class AsyncFutureN(Generic[_FirstType, _SecondType, _ThirdType]):
    """
    Type that provides the required API for ``Future`` to be async.

    Should not be used directly. Use ``FutureBasedN`` instead.
    """

    @abstractmethod
    def __await__(self: _AsyncFutureType) -> Generator[
        Any, Any, io.IOBasedN[_FirstType, _SecondType, _ThirdType],
    ]:
        """Magic method to allow ``await`` expression."""

    @abstractmethod
    async def awaitable(
        self: _AsyncFutureType,
    ) -> io.IOBasedN[_FirstType, _SecondType, _ThirdType]:
        """Underling logic under ``await`` expression."""


#: Type alias for kinds with one type argument.
AsyncFuture1 = AsyncFutureN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
AsyncFuture2 = AsyncFutureN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
AsyncFuture3 = AsyncFutureN[_FirstType, _SecondType, _ThirdType]


class FutureBasedN(
    FutureLikeN[_FirstType, _SecondType, _ThirdType],
    AsyncFutureN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for real ``Future`` objects.

    They can be awaited.
    """


#: Type alias for kinds with one type argument.
FutureBased1 = FutureBasedN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
FutureBased2 = FutureBasedN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
FutureBased3 = FutureBasedN[_FirstType, _SecondType, _ThirdType]
