import os
from pathlib import Path
from logging import Logger

import finac

from tagil import component



@component(
    inject={
        "logger": "accountant_logger"
    }
)
class Accountant:
    DB_PATH = Path("accountant.db")

    def __init__(self, logger: Logger):
        self.logger = logger
        import os
        self.logger.warning(f"{os.getcwd()}")

        finac.init("accountant.db")


if __name__ == '__main__':
    a = Accountant(Logger("bla"))
