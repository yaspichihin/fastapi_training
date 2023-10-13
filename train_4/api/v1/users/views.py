from fastapi import APIRouter

from api.v1.users.schemas import CreateUser
from api.v1.users import utils


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/")
def create_user(new_user: CreateUser):
    return utils.create_user(new_user=new_user)
