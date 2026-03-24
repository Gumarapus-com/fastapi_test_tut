from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import as_declarative
from sqlalchemy.pool import NullPool


@as_declarative()
class DBBase:
    ...


def create_db_engine(db_url: str) -> AsyncEngine:
    # Use `echo=True` to verbosely print DB query
    # return create_async_engine(db_url, poolclass=NullPool, echo=True)
    return create_async_engine(db_url, poolclass=NullPool)


def create_db_session(db_engine) -> async_sessionmaker:
    return async_sessionmaker(db_engine, expire_on_commit=False)
