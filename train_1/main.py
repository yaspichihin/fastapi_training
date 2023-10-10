import uvicorn
from fastapi import FastAPI
from pydantic import EmailStr, BaseModel


app = FastAPI()

# Пример автоматического преобразования в JSON
@app.get('/')
def index():
    return {'message': 'index'}

# Пример автоматического преобразования в JSON
@app.get('/items')
def list_items():
    return ['item 1', 'item 2']

# Должно обязательно идти перед '/items/{item_id}'
# иначе last, будет подставляться вместо item_id
# из-за чего будет ошибка валидации.
@app.get('/items/last')
def get_last():
    return {'item': {'id': 'last'}}

# Параметр пути
@app.get('/items/{item_id}')
def get_item(item_id: int):
    return {'item': {'id': item_id}}

# Параметр запрсоса
@app.get('/query_params')
def get_item(q_param_1: int = 0, q_param_2: str = 'zero'):
    return {q_param_2: q_param_1}

# Пример добавления пользователя через POST
class CreateUser(BaseModel):
    email: EmailStr

@app.post('/users')
def create_user(user: CreateUser):
    return {'message': 'success', 'email': user.email}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
