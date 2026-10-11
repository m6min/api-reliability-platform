from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()

@router.get("/", response_model=list[ProductRead], summary="Get all products from database in a list")
async def get_products(db: Annotated[AsyncSession, Depends(get_db)]) -> list[Product]:
    stmt = select(Product)
    results = await db.execute(stmt)
    products = results.scalars().all()
    return list(products)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Create a new product into database")
async def create_product(product_data: ProductCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    """Create a 'Product' object on database"""
    product = Product(**product_data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Product:
    """Get a 'Product' object from database with an id of integer"""
    stmt = select(Product).where(
        Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No matched product for id of {product_id}")
    return product

@router.put("/{product_id}", response_model=ProductRead, summary="Update a product with id")
async def update_product(product_id: int, product_data: ProductUpdate, db: Annotated[AsyncSession, Depends(get_db)]) -> Product:
    stmt = select(Product).where(
        Product.id == product_id
    )
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No matched product for id of {product_id}")
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete your product with id")
async def delete_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
    stmt = delete(Product).where(
            Product.id == product_id)
    result = await db.execute(stmt)
    if result.rowcount == 0: # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No matched product for id of {product_id}")
    await db.commit()
