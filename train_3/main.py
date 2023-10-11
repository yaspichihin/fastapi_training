import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from models import Base, db_helper
from api import api_router


# Добавим действия до старта приложения и после через lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц
    async with db_helper.engine.begin() as conn:
        # Вызов Base.metadata.create_all без скобок
        await conn.run_sync(Base.metadata.create_all)
    # Передаем управление приложению
    yield
    # Действия после остановки приложения
    pass


app = FastAPI(lifespan=lifespan)
# При регистрации можно переопределть prefix= и tags=
app.include_router(router=api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
