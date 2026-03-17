import pytest
from httpx import AsyncClient, ASGITransport

from app.app import create_app
from app.db import create_db_engine, create_db_session


# This is important, to make different database
# And using `memory` to use fresh empty database for each test
DB_URL = 'sqlite+aiosqlite:///:memory:'


@pytest.fixture
def db_engine():
    engine = create_db_engine(DB_URL)
    return engine


@pytest.fixture
def db_session(db_engine):
    # Create db session maker
    session = create_db_session(db_engine)
    # return db session
    return session()


@pytest.fixture
def app(db_engine):
    return create_app(db_engine=db_engine)


@pytest.fixture
def http(app):
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    )
