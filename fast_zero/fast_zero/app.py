from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from .database import get_session
from .models import User
from .schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from .security import get_password_hash

app = FastAPI()


@app.get('/aula01', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


# retornar um HTML
# status_code -> o que queremos que seja retornado
# response_class -> o tipo de resposta que queremos que seja retornado
@app.get('/aula02', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Olá Mundo!</title>
        </head>
        <body>
            <h1>Olá Mundo!</h1>
        </body>
        </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Nome de usuário já existe',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já existe',
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(limit: int, offset: int, session=Depends(get_session)):
    users = session.execute(select(User).limit(limit).offset(offset))
    users = users.scalars().all()

    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!'}
