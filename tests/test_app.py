from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (Preparação)

    # Act (Ação)
    response = client.get('/')

    # Assert (Verificação)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}

    # teardown (Limpeza) - Não é necessário
