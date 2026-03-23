import asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)
from sqlalchemy.orm import as_declarative
from sqlalchemy.pool import NullPool


@as_declarative()
class DBBase:
    ...


def create_db_engine(db_url: str):
    return create_async_engine(db_url, poolclass=NullPool, echo=True)


def create_db_session(db_engine):
    return async_sessionmaker(db_engine, expire_on_commit=False)
