from fastapi import APIRouter, Path
from typing import Annotated


items_router = APIRouter(prefix="/items", tags=["items"])


@items_router.get("/")
def list_items():
    return ["item 1", "item 2"]


# Должно обязательно идти перед '/{item_id}'
# иначе last, будет подставляться вместо item_id
# из-за чего будет ошибка валидации.
@items_router.get("/last/")
def get_last():
    return {"item": {"id": "last"}}


# Параметр пути
# Добавили аннотацию, что item_id мб более равен 1 и меньше 1_000_000
@items_router.get("/{item_id}/")
def get_item(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {"item": {"id": item_id}}
