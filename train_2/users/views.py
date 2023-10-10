from fastapi import APIRouter

from users.schemas import CreateUser
from users import crud


users_router = APIRouter(prefix='/users', tags=['users'])

@users_router.post('/')
def create_user(new_user: CreateUser):
    return crud.create_user(new_user=new_user)
