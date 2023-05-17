from logging import Logger

from tagil import component


@component()
class AccountingService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
