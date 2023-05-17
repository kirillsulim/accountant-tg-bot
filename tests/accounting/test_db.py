import pytest

from sqlalchemy import (
    create_engine,
    select,
    text,
)
from sqlalchemy.orm import (
    Session,
)

from accounting.model import (
    Account,
    Base,
)


class TestDb:
    @pytest.fixture(scope="session")
    def engine(self):
        db = create_engine(f"sqlite://", echo=True)
        try:
            Base.metadata.create_all(db)
            yield db
        finally:
            db.dispose()

    @pytest.fixture(scope="function")
    def session(self, engine):
        with Session(engine) as session:
            yield session
            session.rollback()

    def test_session(self, session):
        result = session.execute(text("SELECT 1;"))
        assert result.first()[0] == 1

    def test_create_account(self, session):
        account = Account(name="Test account")
        session.add(account)
        session.flush()

        result = session.scalars(select(Account))
        assert result.first().name == "Test account"
