import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

import models as mdl


async def create_user(session: AsyncSession, username: str) -> mdl.User:
    user = mdl.User(username=username)
    session.add(user)
    await session.commit()
    print(user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> mdl.User | None:
    stmt = select(mdl.User).filter(mdl.User.username == username)
    result: Result = await session.execute(stmt)
    user: mdl.User | None = result.scalar_one_or_none()
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str,
    last_name: str,
) -> mdl.Profile:
    profile = mdl.Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> None:
    # Добавляем options(joinedload(mdl.User.profile)) т.к. в asyncio
    # Критично не делать доп запросов, лучше сразу подгрузить всю информацию
    stmt = select(mdl.User).options(joinedload(mdl.User.profile)).order_by(mdl.User.id)
    result: Result = await session.execute(stmt)
    users: list[mdl.User] = result.scalars().all()
    for user in users:
        print(f"{user}. Profiles:{user.profile}")


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[mdl.Post]:
    posts = [mdl.Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(session: AsyncSession,):
    # Подгрузка через join, 1 запрос, но дублирование информации и не забывать про .unique()
    # joinedload часто используют для связи 1к1
    stmt = select(mdl.User).options(joinedload(mdl.User.posts)).order_by(mdl.User.id)

    # Подгрузка через доп запрос, позволяет уйти от .unique() часто используют для связи ко многим
    # stmt = select(mdl.User).options(selectinload(mdl.User.posts)).order_by(mdl.User.id)

    users = await session.scalars(stmt)

    # Пример через Result вместо users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()

    # .unique() добавили для ухода от sqlalchemy.exc.InvalidRequestError: The unique() method
    # must be invoked on this Result, as it contains results that include joined eager loads
    # against collections, тем самым показали, что должен быть уникален пользователь
    for user in users.unique():
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(mdl.Post).options(joinedload(mdl.Post.user)).order_by(mdl.Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(f"{post=}")
        print(f"{post.user=}")


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(mdl.User)
        .options(
            joinedload(mdl.User.profile),
            selectinload(mdl.User.posts),
        )
        .order_by(mdl.User.id)
    )
    users = await session.scalars(stmt)

    for user in users.unique():
        print(user)
        print(user.profile.last_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):

    # Если требуется фильтровать, тьо можно сделать join() для фильтрации.
    # а joinedload ио же остается для загрузки связанных данных
    stmt = (
        select(mdl.Profile)
        # Пример последовательных запросов
        .options(joinedload(mdl.Profile.user).selectinload(mdl.User.posts))
        .order_by(mdl.Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.last_name)
        print(profile.user.posts)


async def main_relations(session: AsyncSession):
    # Создание пользователей
    # await create_user(session=session, username="Sam")
    # await create_user(session=session, username="Din")
    # await create_user(session=session, username="Alice")

    # Получаем пользователей
    user_sam = await get_user_by_username(session, "Sam")
    user_din = await get_user_by_username(session, "Din")
    user_alice = await get_user_by_username(session, "Alice")

    # Добавляем профили
    # await create_user_profile(
    #     session=session,
    #     user_id=user_sam.id,
    #     first_name="Sam",
    #     last_name="Black",
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_din.id,
    #     first_name="Din",
    #     last_name="Black",
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_alice.id,
    #     first_name="Alice",
    #     last_name="White",
    # )

    # Просмотрим пользователей с информацией о их профайлах
    await show_users_with_profiles(session)
    # User(self.id=1, self.username='Sam'). Profiles:<models.profile.Profile object at 0x000001FE5BD02250>
    # User(self.id=2, self.username='Din'). Profiles:<models.profile.Profile object at 0x000001FE5BD022D0>

    # Создадим посты пользователей
    # await create_posts(session, user_sam.id, "SQL 2.0", "SQL Joins")
    # await create_posts(session, user_din.id, "SQL 1.0", "SQL Select")


    # Распечатать пользователя и его посты
    await get_users_with_posts(session)

    # Распечатать пост и его автора
    await get_posts_with_authors(session)

    # Распечатать пользователя, его профайл и его статьи
    await get_users_with_posts_and_profiles(session)

    # Получить информацию по профайлу и постам пользователя
    await get_profiles_with_users_and_users_with_posts(session)


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> mdl.Order:
    order = mdl.Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str, 
    price: int,
) -> mdl.Product:
    product = mdl.Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product
    

async def demo_m2m(session: AsyncSession):
    # Создадим пару заказов
    order_1 = await create_order(session)
    order_2 = await create_order(session, promocode="promo")
    
    # Создадим пару продуктов
    product_1 = await create_product(session, "product_1", "product_1_dsc", 1)
    product_2 = await create_product(session, "product_2", "product_2_dsc", 2)
    product_3 = await create_product(session, "product_3", "product_3_dsc", 3)

    # Объединим продукты и товары

    # Для подгрузки Order.products для работы связка m2m, по умолчанию получает данные из кэша
    # Когда данные требуются именно из таблицы лучше использовать scalars
    # order_1 = await session.get(mdl.Order, order_1.id, options=(selectinload(mdl.Order.products)))
    # order_2 = await session.get(mdl.Order, order_2.id, options=(selectinload(mdl.Order.products)))
    order_1 = await session.scalar(
        select(mdl.Order)
        .where(mdl.Order.id == order_1.id)
        .options(selectinload(mdl.Order.products))
    )
    order_2 = await session.scalar(
        select(mdl.Order)
        .where(mdl.Order.id == order_2.id)
        .options(selectinload(mdl.Order.products))
    )

    # Добавление продуктов в звказы
    order_1.products.append(product_1)
    order_2.products.append(product_1)
    order_2.products.append(product_2)
    # Альтернатива через перепримваивание
    # order_2.products = [product_1, product_2]

    # Сохраним изменения
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[mdl.Order]:
    query = select(mdl.Order).options(selectinload(mdl.Order.products)).order_by(mdl.Order.id)
    orders: Result = await session.scalars(query)
    return list(orders)


async def get_orders_with_products_through_secondary(session: AsyncSession) -> None:
    orders = await get_orders_with_products(session)
    for order in orders:
        print(f"{order.id=}")
        for product in order.products:
            print(f"--> {product.name=}")
    # order.id=3
    # --> product.name='product_1'
    # order.id=4
    # --> product.name='product_1'
    # --> product.name='product_2'


async def get_orders_with_products_with_association(session: AsyncSession) -> list[mdl.Order]:
    stmt = (
        select(mdl.Order)
        .options(
            selectinload(mdl.Order.products_details)
            .joinedload(mdl.OrderProductAssociation.product)
        )
        .order_by(mdl.Order.id))
    orders: Result = await session.scalars(stmt)
    return list(orders)


# Еще один print заказов и продуктов
async def another_func(session: AsyncSession) -> None:
    orders = await get_orders_with_products_with_association(session=session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for order_product_details in order.products_details: # type: mdl.OrderProductAssociation
            # Для order_product_details.product нужно специально еще указывать
            # .joinedload(mdl.OrderProductAssociation.product) для подгрузки данных
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty:", order_product_details.count,
            )
    # 3 None 2023-10-25 16:47:21.744829 products:
    # - 4 product_1 1 qty: 1
    # 4 promo 2023-10-25 16:47:21.751829 products:
    # - 4 product_1 1 qty: 1
    # - 5 product_2 2 qty: 1


# Пример функции добавления 1 подарка ко всем заказам
async def add_gift_to_all_orders(session: AsyncSession) -> None:
    # Получим все заказы
    orders = await get_orders_with_products_with_association(session)

    # Создадим подарок
    gift = await create_product(session, "gift", "gift_desc", 0)

    # Добавим подарок
    for order in orders:
        order.products_details.append(
            mdl.OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift
                # order прописывать не нужно т.к. добавляем
                # уже через связь order (order.products_details)
            )
        )




async def main():
    async with mdl.db_helper.session_factory() as session:
        # await add_gift_to_all_orders(session)
        await another_func(session)





if __name__ == "__main__":
    asyncio.run(main())
