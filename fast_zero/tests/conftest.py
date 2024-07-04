import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    # gerenciador de contexto
    # yeild -> retorna o valor e continua a execução
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
