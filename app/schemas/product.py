from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(examples=["Iphone 18 Pro"])
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2, examples=["1250"])
    stock: int = Field(default=0,ge=0, examples=[82])

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(ProductBase):
    pass