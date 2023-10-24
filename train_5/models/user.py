from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

# Импорт только при проверке типов, уходим от
# циклического импорта между моделями Post и User
if TYPE_CHECKING:
    from models.post import Post
    from models.profile import Profile

# В данном случае связь между User и Post "Один ко многим"
# у одного пользователя мб много постов, а у поста мб 1 пользователь


class User(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id=}, {self.username=!r})"
