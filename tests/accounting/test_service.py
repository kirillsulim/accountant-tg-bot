import asyncio

import pytest
import pytest_asyncio

from sqlalchemy import (
    create_engine,
    text,
    select,
)
from sqlalchemy.orm import (
    Session,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from db.database_initializer import DatabaseInitializer
from db.model import (
    Base,
    Account,
)
from accounting.service import AccountingService
from db.session_factory import SessionFactory


class TestAccountingService:
    @pytest.fixture(scope="session")
    def event_loop(self):
        policy = asyncio.get_event_loop_policy()
        loop = policy.new_event_loop()
        yield loop
        loop.close()


    @pytest_asyncio.fixture(scope="session")
    def engine(self):
        engine = create_async_engine(url="sqlite+aiosqlite://")
        yield engine
        engine.sync_engine.dispose()

    @pytest_asyncio.fixture(scope="session")
    async def init_db(self, engine):
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

    @pytest_asyncio.fixture(scope="session")
    async def session(self, engine, init_db):
        async_session = async_sessionmaker(engine)
        async with async_session() as session:
            yield session

    @pytest.mark.asyncio
    async def test_session(self, session):
        acc = Account(name="Blabla")
        session.add_all([acc])
        await session.commit()

        assert len((await session.execute(select(Account))).scalars().all()) == 2


    @pytest.mark.asyncio
    async def test_create_account(self, service):
        account = await service.create_account("test-account")

        assert account.name == "test-account"

