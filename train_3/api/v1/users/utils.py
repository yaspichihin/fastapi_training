from api.v1.users.schemas import CreateUser


def create_user(new_user: CreateUser) -> dict:
    # Делаем словарь из объекта через model_dump()
    new_user = new_user.model_dump()
    return {"success": True, "user": new_user}
