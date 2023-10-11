from fastapi import APIRouter

from api.v1.items.views import items_router
from api.v1.users.views import users_router
from api.v1.products.views import products_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(router=items_router)
v1_router.include_router(router=users_router)
v1_router.include_router(router=products_router)
