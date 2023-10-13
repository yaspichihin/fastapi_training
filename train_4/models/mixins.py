from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

# Импорт только при проверке типов
if TYPE_CHECKING:
    from models import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_id_nullable: bool = False

    @declared_attr
    def user_id(cls) -> Mapped[str]:
        return mapped_column(ForeignKey("users.id"), unique=cls._user_id_unique)

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User", back_populates=cls._user_back_populates)
