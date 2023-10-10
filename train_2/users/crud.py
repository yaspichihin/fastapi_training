from users.schemas import CreateUser


def create_user(new_user: CreateUser) -> dict:
    # Делаем словарь из данных
    new_user = new_user.model_dump()
    return {'success': True, 'user': new_user}
