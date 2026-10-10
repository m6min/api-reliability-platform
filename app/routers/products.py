from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/")
def get_products():
    return {"live": "true"}