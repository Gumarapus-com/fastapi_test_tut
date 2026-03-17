import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import as_declarative


@as_declarative()
class DBBaseClass:
    ...


def create_db_engine(db_url: str):
    return create_async_engine(db_url)


def create_db_session(db_engine):
    return async_sessionmaker(db_engine)
