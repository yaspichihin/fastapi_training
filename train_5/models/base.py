from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    # Указываем что модель абстрактная и таблицы быть не должно
    __abstract__ = True

    # Автоматическое формирование имени таблицы
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    # Добавляем колонки по умолчанию для дочерних таблиц
    # альтернативный вариант через Mixin
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
