from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession
)

from app.app import create_app
from app.crud import create_note, get_note_by_id
from app.db import create_db_engine, create_db_session
from app.db_tables import DBBase


# This is important, to make different database
# And using `memory` to use fresh empty database for each test
# DB_URL = 'sqlite+aiosqlite:///:memory:'
DB_URL = 'sqlite+aiosqlite:///test.db'
# pytestmark = pytest.mark.anyio

engine = create_db_engine(DB_URL)


# @pytest.fixture(scope="session")
# def anyio_backend():
#     return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    async with engine.begin() as conn:
        await conn.run_sync(DBBase.metadata.drop_all)
        await conn.run_sync(DBBase.metadata.create_all)
        yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_session_maker(db_engine):
    async with db_engine.connect() as conn:
        yield create_db_session(conn)


@pytest_asyncio.fixture(scope='function')
# def db_session(db_session_maker) -> AsyncGenerator[AsyncSession, None]:
async def db_session(db_session_maker) -> AsyncSession:
    # async_session = AsyncSession(bind=db_connection)
    async with db_session_maker() as sess:
        yield sess


@pytest.fixture
def app(db_engine, db_session_maker):
    return create_app(db_engine, db_session_maker)


@pytest_asyncio.fixture()
async def http(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as http_client:
        yield http_client


@pytest_asyncio.fixture()
async def a_note(db_session):
    return (
        await get_note_by_id(db_session, 1)
        or await create_note(db_session, 'A Note', 'Has description')
    )
