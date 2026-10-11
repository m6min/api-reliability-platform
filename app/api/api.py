from fastapi import APIRouter

from app.routers import products

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["Product Actions"])
