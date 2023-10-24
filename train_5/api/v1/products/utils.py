from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product
from api.v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


async def list_products(session: AsyncSession) -> list[Product]:
    query = select(Product, Product.id).order_by(Product.id)
    result: Result = await session.execute(query)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    query = select(Product).filter(Product.id == product_id)
    result: Result = await session.execute(query)
    product = result.scalar_one_or_none()
    return product


async def create_product(session: AsyncSession, new_product: ProductCreate) -> Product:
    # Через model_dump превращаем данные в словарь и распаковываем в объект продуктов
    new_product = Product(**new_product.model_dump())
    session.add(new_product)
    await session.commit()
    return new_product


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    # exclude_unset=True - исключаем значения, что не были переданы
    # тем сымым регулируем методы PUT и PATCH, если partial=False, то PUT
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()
