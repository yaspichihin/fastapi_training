from models.base import Base

# Добавление моделей
from models.product import Product
from models.user import User
from models.post import Post
from models.profile import Profile

# Класс и объект для работы с БД
from models.db_helper import DBHelper, db_helper
