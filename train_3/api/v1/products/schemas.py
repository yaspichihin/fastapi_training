from pydantic import BaseModel, ConfigDict


# Схема основа
# id не указываем, что бы при создании пользователь
# не увидел в схеме возможность добавитьсвой id
class ProductBase(BaseModel):
    name: str
    description: str
    price: int


# Схема для создания продукта
class ProductCreate(ProductBase):
    pass


# Схема для обновления продукта мнтодом PUT
class ProductUpdate(ProductCreate):
    pass


# Схема для обновления продукта мнтодом PATCH
class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


# Схема для возврата продукта
class Product(ProductBase):
    # Указываем что данные можно брать из атрибутов объекта
    # Используется при указании возвращаемого типа во view
    model_config = ConfigDict(from_attributes=True)

    id: int
