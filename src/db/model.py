from typing import List
from enum import (
    Enum as PyEnum,
    auto,
    unique,
)

from sqlalchemy import (
    Enum,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)

    records: Mapped[List["Record"]] = relationship(back_populates="account")
    active_transactions: Mapped[List["Transaction"]] = relationship(back_populates="approver")


@unique
class TransactionState(PyEnum):
    STARTED = auto()
    ACCEPTED = auto()
    DECLINED = auto()


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    state: Mapped[TransactionState] = mapped_column(Enum(TransactionState))

    approver_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    approver: Mapped[Account] = relationship(back_populates="active_transactions")

    records: Mapped[List["Record"]] = relationship(back_populates="transaction")


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped[Account] = relationship(back_populates="records")
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transaction.id"))
    transaction: Mapped[Transaction] = relationship(back_populates="records")
