from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.product_repository import (
    delete_product_by_id,
    get_all_products,
    get_product_by_id,
    save_product,
    update_product_by_id,
)
from app.schemas.product import ProductUpdate


def make_product(name: str = "Keyboard") -> Product:
    return Product(
        name=name,
        description="Mechanical keyboard",
        price=Decimal("99.90"),
        stock=10,
    )


@pytest.mark.asyncio
async def test_save_product_persists_product(
    repository_db_session: AsyncSession,
) -> None:
    product = make_product()

    saved_product = await save_product(repository_db_session, product)

    assert saved_product.id is not None
    assert saved_product.name == "Keyboard"
    assert saved_product.price == Decimal("99.90")


@pytest.mark.asyncio
async def test_get_all_products_returns_saved_products(
    repository_db_session: AsyncSession,
) -> None:
    await save_product(repository_db_session, make_product("Keyboard"))
    await save_product(repository_db_session, make_product("Mouse"))

    products = await get_all_products(repository_db_session)

    assert len(products) == 2
    assert {product.name for product in products} == {"Keyboard", "Mouse"}


@pytest.mark.asyncio
async def test_get_product_by_id_returns_matching_product(
    repository_db_session: AsyncSession,
) -> None:
    saved_product = await save_product(
        repository_db_session,
        make_product(),
    )

    product = await get_product_by_id(
        repository_db_session,
        saved_product.id,
    )

    assert product is not None
    assert product.id == saved_product.id
    assert product.name == "Keyboard"


@pytest.mark.asyncio
async def test_update_product_changes_existing_product(
    repository_db_session: AsyncSession,
) -> None:
    saved_product = await save_product(
        repository_db_session,
        make_product(),
    )
    update_data = ProductUpdate(
        name="Updated keyboard",
        description="Updated description",
        price=Decimal("109.90"),
        stock=12,
    )

    updated_product = await update_product_by_id(
        repository_db_session,
        update_data,
        saved_product.id,
    )

    assert updated_product is not None
    assert updated_product.name == "Updated keyboard"
    assert updated_product.price == Decimal("109.90")
    assert updated_product.stock == 12


@pytest.mark.asyncio
async def test_delete_product_removes_existing_product(
    repository_db_session: AsyncSession,
) -> None:
    saved_product = await save_product(
        repository_db_session,
        make_product(),
    )

    deleted = await delete_product_by_id(
        repository_db_session,
        saved_product.id,
    )
    deleted_product = await get_product_by_id(
        repository_db_session,
        saved_product.id,
    )

    assert deleted is True
    assert deleted_product is None


@pytest.mark.asyncio
async def test_delete_product_returns_false_for_missing_product(
    repository_db_session: AsyncSession,
) -> None:
    deleted = await delete_product_by_id(
        repository_db_session,
        product_id=999,
    )

    assert deleted is False
