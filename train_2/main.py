import uvicorn
from fastapi import FastAPI

from items_view import items_router
from users.views import users_router

app = FastAPI()
# При регистрации можно переопределть prefix= и tags=
app.include_router(items_router, prefix='/items')
app.include_router(users_router)

# Пример автоматического преобразования в JSON
@app.get('/')
def index():
    return {'message': 'index'}

# Параметр запрсоса
@app.get('/query_params')
def get_item(q_param_1: int = 0, q_param_2: str = 'zero'):
    return {q_param_2: q_param_1}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
