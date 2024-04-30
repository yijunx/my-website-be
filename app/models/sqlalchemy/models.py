from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.sqlalchemy.base import Base


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # property
    sessions: Mapped[list["SessionORM"]] = relationship(
        "SessionORM",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    accounts: Mapped[list["AccountORM"]] = relationship(
        "AccountORM",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )


class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), ondelete="CASCADE")
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_account_id: Mapped[str] = mapped_column(String, nullable=False)

    # property
    user = relationship("UserORM", back_populates="accounts")


class SessionORM(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), ondelete="CASCADE")
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)


    # property
    user = relationship("UserORM", back_populates="sessions")




class VerificationTokenORM(Base):
    __tablename__ = "verification_tokens"

    