from models.base import Base

# Добавление моделей
from models.product import Product
from models.user import User
from models.post import Post
from models.profile import Profile
from models.order import Order

# Перешли к классу
# from models.order_product_association import order_product_association
from models.order_product_association import OrderProductAssociation

# Класс и объект для работы с БД
from models.db_helper import DBHelper, db_helper
