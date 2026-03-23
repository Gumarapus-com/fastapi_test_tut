from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .db import create_db_engine, create_db_session, DBBase
from .routers import router


_db_engine = create_db_engine('sqlite+aiosqlite:///db.sqlite')
_db_session_maker = create_db_session(_db_engine)


def create_app(
    db_session_maker: async_sessionmaker[AsyncSession] | None = _db_session_maker
) -> FastAPI:
    if db_session_maker is None:
        db_engine = _db_engine
        db_session_maker = _db_session_maker
    else:
        db_engine = None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # On start up
        #  Create database tables on start up
        async with db_session_maker().begin() as conn:
            await conn.run_sync(DBBase.metadata.create_all)

        # on process
        yield

        # On shutdown
        #  dispose DB connection pools
        if db_engine is not None:
            await db_engine.dispose()

    app = FastAPI(
        debug=True,
        description='Simple Rest API',
        lifespan=lifespan
    )
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
