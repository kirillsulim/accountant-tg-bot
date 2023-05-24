from typing import (
    Callable,
    TypeVar,
    Awaitable,
)

from tagil import component
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


T = TypeVar("T")


@component
class SessionFactory:
    def __init__(self, url):
        self.engine = create_async_engine(url)
        self.async_session = async_sessionmaker(self.engine)

    async def run_with_session(self, action: Callable[[AsyncSession], Awaitable[T]]) -> Awaitable[T]:
        async with self.async_session() as session:
            return await action(session)
