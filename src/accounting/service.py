from logging import Logger
from typing import Awaitable

from sqlalchemy.ext.asyncio import AsyncSession
from tagil import component

from db.model import (
    Account,
    Transaction,
)
from db.session_factory import SessionFactory


@component()
class AccountingService:
    def __init__(self, session_factory: SessionFactory):
        self.logger = Logger(self.__class__.__name__)
        self.session_factory = session_factory

    async def create_account(self, name) -> Awaitable[Account]:
        async def _create_account(session: AsyncSession):
            account = Account(name=name)
            session.add(account)

            await session.commit()

            return account

        return await self.session_factory.run_with_session(_create_account)

    async def transfer(self, src: Account, dest: Account, cents_amount: int) -> Awaitable[Transaction]:
        pass

    async def rollback(self, transaction: Transaction) -> Awaitable[None]:
        pass

    async def commit(self, transaction: Transaction) -> Awaitable[None]:
        pass

    async def balance(self, account: Account):
        pass
