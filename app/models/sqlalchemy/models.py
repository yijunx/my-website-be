from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.sqlalchemy.base import Base

# these tables are inspired by prisma schema


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    role: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # property
    sessions: Mapped[list["LoginSessionORM"]] = relationship(
        "LoginSessionORM",
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
    __table_args__ = (
        Index("provider_and_provider_account_id", "provider", "provider_account_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_account_id: Mapped[str] = mapped_column(String, nullable=False)

    # property
    user = relationship("UserORM", back_populates="accounts")


class LoginSessionORM(Base):
    __tablename__ = "login_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # property
    user = relationship("UserORM", back_populates="sessions")


class VerificationTokenORM(Base):
    __tablename__ = "verification_tokens"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    identifier: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)
