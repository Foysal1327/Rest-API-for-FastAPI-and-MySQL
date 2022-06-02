from fastapi import APIRouter
from controller import product, user

router = APIRouter()
router.include_router(product.router)
router.include_router(user.router)