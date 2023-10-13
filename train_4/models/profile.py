# from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import UserRelationMixin

# Переделали через UserRelationMixin
# Импорт только при проверке типов, уходим от
# циклического импорта между моделями Post и User
# if TYPE_CHECKING:
#     from models import User


class Profile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))

    # Переделали через UserRelationMixin
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
