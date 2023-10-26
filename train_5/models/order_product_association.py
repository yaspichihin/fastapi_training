from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


if TYPE_CHECKING:
    from models.order import Order
    from models.product import Product

# Аcсоциативный класс для m2m
class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # Дополнительные столбцы
    
    # Количество данного товара в данном заказе
    count: Mapped[int] = mapped_column(default=1, server_default="1")

    # Фиксация цены в рамках одного заказа т.к. цена может
    # измениться для магазина, но не должна меняться для заказа
    unit_price: Mapped[int] = mapped_column(default=1, server_default="1")

    # Связь между Ассоциациями и наследникоами
    order: Mapped["Order"] = relationship(back_populates="products_details")
    product: Mapped["Product"] = relationship(back_populates="orders_details")



# # Аcсоциативную таблицу выполнять через Core для простой m2m
# order_product_association = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("orders.id"), nullable=False),
#     Column("product_id", ForeignKey("products.id"), nullable=False),

#     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
# )





