from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserBD, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hello world!'}


@app.get('/html', response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Ola mundo</title>
        </head>
        <body>
            <h1>Hello world!</h1>
        </body>
    </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserBD(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id
