from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from api.v1.products import utils
from api.v1.products import dependecies
from api.v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)


products_router = APIRouter(prefix="/products", tags=["products"])


# LIST
@products_router.get(
    "/",
    response_model=list[Product],
)
async def list_products(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await utils.list_products(session=session)


# GET
@products_router.get(
    "/{product_id}/",
    response_model=Product,
)
async def get_product(
    product: Product = Depends(dependecies.get_product),
):
    return product


# CREATE
@products_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Product,
)
async def create_product(
    new_product: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await utils.create_product(session=session, new_product=new_product)


# PUT
@products_router.put(
    "/{product_id}/",
    response_model=None,
)
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(dependecies.get_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await utils.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


# Patch
@products_router.patch(
    "/{product_id}/",
    response_model=None,
)
async def update_product(
    product_update: ProductUpdatePartial,
    product: Product = Depends(dependecies.get_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await utils.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


# Delete
@products_router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def update_product(
    product: Product = Depends(dependecies.get_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await utils.delete_product(
        session=session,
        product=product,
    )
