from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware, now_utc
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, Float, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column

DATABASE_URL = "sqlite+aiosqlite:///./my_database.db"
Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=8.0)
    registered_at = Column(TIMESTAMP, default=datetime.now())
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class CryptoCard(Base):
    __tablename__ = "crypto_card"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price_sell = Column(Float, nullable=False)
    price_buy = Column(Float, nullable=False)


class UserCryptoCard(Base):
    __tablename__ = "user_crypto_card"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    crypto_card_id = Column(Integer, ForeignKey("crypto_card.id"))
    amount = Column(Integer, nullable=False, default=0)


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    token: Mapped[str] = mapped_column(String(length=43), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id, ondelete="cascade"), nullable=False
    )


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[None, AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
