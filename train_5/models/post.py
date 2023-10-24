# from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import UserRelationMixin

# Переделали через UserRelationMixin
# Импорт только при проверке типов, уходим от
# циклического импорта между моделями Post и User
# if TYPE_CHECKING:
#     from models import User

# relationship не вносят изменения в таблицы,
# а только упрощают работу с ORM.

# В данном случае связь между User и Post "Один ко многим"
# у одного пользователя мб много постов, а у поста мб 1 пользователь


class Post(Base, UserRelationMixin):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    # Переделали через UserRelationMixin
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id=}, {self.title=!r}, {self.user_id=})"

