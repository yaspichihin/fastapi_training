from typing import TYPE_CHECKING
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime as dt

from models.base import Base

# Закомментировали т.к. делаем через класс
# from models.order_product_association import order_product_association

# Импорт только при проверке типов, уходим от
# циклического импорта между моделями Product и Order
if TYPE_CHECKING:
    from models.product import Product
    from models.order_product_association import OrderProductAssociation

class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[dt] = mapped_column(default=dt.utcnow, server_default=func.now())



    ### Пример 2х связок используется либо 1, либо 2

    # Делаем связку через промежуточную таблицу m2m
    products: Mapped[list["Product"]] = relationship(
        
        # Для варианта через Core
        # secondary=order_product_association,
        
        # Указывает через строку, чтобы алхимия нашда таблицу в Postgre
        secondary="order_product_association",
        back_populates="orders"
    )

    # Делаем дополнительную связку с таблицей ассоциации
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
