from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='test', password='test', email='teste@teste.com')

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'teste@teste.com')
    )

    assert result.username == 'test'
