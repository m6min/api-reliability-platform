from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.product import ProductCreate


def test_product_create_accepts_valid_data() -> None:
    product = ProductCreate(
        name="Keyboard",
        description="Mechanical keyboard",
        price="99.90",
        stock=10,
    )

    assert product.name == "Keyboard"
    assert product.price == Decimal("99.90")
    assert product.stock == 10


def test_product_create_rejects_invalid_price() -> None:
    with pytest.raises(ValidationError):
        ProductCreate(
            name="Keyboard",
            description="Mechanical keyboard",
            price="abc",
            stock=10,
        )
