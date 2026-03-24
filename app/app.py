from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .db import create_db_engine, create_db_session, DBBase
from .routers import router

DB_URL = 'sqlite+aiosqlite:///db.sqlite'


def create_app(
    db_engine: AsyncEngine = create_db_engine(DB_URL),
    db_session_maker: async_sessionmaker[AsyncSession] | None = None
) -> FastAPI:
    if db_session_maker is None:
        db_session_maker = create_db_session(db_engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # On start up
        #  Create database tables on start up
        async with db_engine.connect() as conn:
            await conn.run_sync(DBBase.metadata.create_all)

        # on process
        yield

        # On shutdown
        #  dispose DB connection pools
        if db_engine is not None:
            await db_engine.dispose()

    app = FastAPI(description='Simple Rest API', lifespan=lifespan)
    app.include_router(router)

    @app.middleware('http')
    async def middleware_db_session(request: Request, call_next):
        """Create a db session for each request"""
        # Open a DB session
        request.state.db = db_session_maker()

        # Continue the request process
        response = await call_next(request)

        try:
            # Close the DB session
            await request.state.db.close()
        except:
            # ignore exception
            ...

        return response

    return app
