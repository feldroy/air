from collections.abc import Awaitable

type MaybeAwaitable[T] = T | Awaitable[T]
