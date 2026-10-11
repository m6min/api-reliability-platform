from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.base import Base
from app.models.product import Product  # noqa: F401


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
