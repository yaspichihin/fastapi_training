from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from models.base import Base

# Закомментировали т.к. делаем через класс
# from models.order_product_association import order_product_association


# Импорт только при проверке типов, уходим от
# циклического импорта между моделями Product и Order
if TYPE_CHECKING:
    from models.order import Order
    from models.order_product_association import OrderProductAssociation

class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    # Делаем связку через промежуточную таблицу m2m
    orders: Mapped[list["Order"]] = relationship(
        # secondary=order_product_association,
        secondary="order_product_association",
        back_populates="products"
    )

    # Делаем дополнительную связку с таблицей ассоциации
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
