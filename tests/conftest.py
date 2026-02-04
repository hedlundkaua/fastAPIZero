from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry


@contextmanager
def _moc_db_time(*, model, time=datetime(2026, 2, 1)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'create_at'):
            target.created_at = time
        if hasattr(target, 'update_at'):
            target.update_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _moc_db_time


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # aqui ele faz com que o nosso BD fique na memoria ao
        # invés de ser o BD real
        app.dependency_overrides[get_session] = get_session_override
        yield client  # continua no contexto do BD em memoria
    # limpa o BD em memoria para que possamos fazer novos testes
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()
