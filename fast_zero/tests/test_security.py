from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_acess_token():
    data = {'sub': 'test'}

    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clear_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['access_token']
    assert token['token_type'] == 'bearer'


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }
