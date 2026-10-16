from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductUpdate


async def get_all_products(db: AsyncSession) -> list[Product]:
    try:
        stmt = select(Product)
        results = await db.execute(stmt)
        products = results.scalars().all()
        return list(products)
    except SQLAlchemyError:
        await db.rollback()
        raise

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    """Get a 'Product' object from database with an id of integer"""
    try:
        stmt = select(Product).where(
                Product.id == product_id)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        return product
    except SQLAlchemyError:
        await db.rollback()
        raise

async def save_product(db: AsyncSession, product: Product) -> Product:
    try:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    except SQLAlchemyError:
        await db.rollback()
        raise

async def update_product_by_id(db: AsyncSession, product_data: ProductUpdate, product_id: int) -> Product | None:
    try:
        stmt = select(Product).where(
                Product.id == product_id
            )
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        if product is None:
            await db.rollback()
            return None
        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product
    except SQLAlchemyError:
        await db.rollback()
        raise

async def delete_product_by_id(db: AsyncSession, product_id: int) -> bool:
    try:
        stmt = delete(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        if result.rowcount == 0:  # type: ignore
            await db.rollback()
            return False
        await db.commit()
        return True
    except SQLAlchemyError:
        await db.rollback()
        raise
