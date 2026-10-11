from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api import api_router
from app.db.init_db import create_tables
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Lifespan of FastAPI application:
    - Creates tables if not existing
    """
    await create_tables(engine)
    yield
    await engine.dispose()

app = FastAPI(title="Test API", version="1.0", lifespan=lifespan)

app.include_router(api_router, prefix="/api")
