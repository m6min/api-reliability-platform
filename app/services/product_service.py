from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.product_repository import (
    delete_product_by_id,
    save_product,
    update_product_by_id,
)
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
    """Create a 'Product' object on database"""
    product = Product(**product_data.model_dump())
    return await save_product(db, product)

async def update_product(db: AsyncSession, product_id: int, product_data: ProductUpdate,) -> Product | None:
    return await update_product_by_id(
        db=db,
        product_id=product_id,
        product_data=product_data,
    )

async def delete_product(db: AsyncSession, product_id: int) -> bool:
    return await delete_product_by_id(
        db=db,
        product_id=product_id,
    )
