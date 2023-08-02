from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from tagil import component

from db.model import Base
from db.session_factory import SessionFactory


@component
class DatabaseInitializer:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    async def init_db(self):
        async def _init_db(session: AsyncSession):
            await session.run_sync(lambda session: Base.metadata.create_all(session.bind))

        await self.session_factory.run_with_session(_init_db)
        stop = True
