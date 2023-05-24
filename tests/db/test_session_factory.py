import sys
from typing import Awaitable

import pytest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_factory import SessionFactory


class DemoService:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    async def select_1(self) -> Awaitable[int]:
        async def select_1(session: AsyncSession) -> Awaitable[int]:
            result = await session.execute(text("SELECT 1;"))
            return result.first()[0]

        return self.session_factory.run_with_session(select_1)


class TestDbAsync:
    @pytest.mark.asyncio
    async def test_bla(self):
        ds = DemoService(session_factory=SessionFactory("sqlite+aiosqlite://"))
        rs = await ds.select_1()
        print(await rs)
