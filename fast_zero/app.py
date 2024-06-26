from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/aula01', response_model=Message)
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
