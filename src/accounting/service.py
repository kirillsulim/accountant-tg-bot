from logging import Logger

from tagil import component

from accounting.model import (
    Account,
    Transaction,
    Record,
)


@component()
class AccountingService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    async def create_account(self, name) -> Account:
        pass

    async def transfer(self, src: Account, dest: Account, cents_amount: int) -> Transaction:
        pass

    async def rollback(self, transaction: Transaction):
        pass

    async def commit(self, transaction: Transaction):
        pass

    async def balance(self, account: Account):
        pass
