from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import EmailStr, BaseModel, Field


class CreateUser(BaseModel):
    # Старый тип аннотации
    # username: str = Field(..., min_length=3, max_length=20)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
