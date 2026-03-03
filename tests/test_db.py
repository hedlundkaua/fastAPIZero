from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user):
    todo = Todo(
        title='Test todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )
    session.add(todo)
    await session.commit()

    todo = await session.scalar(select(Todo))
    result = asdict(todo)

    result = asdict(todo)

    # 1. Validação Rígida (O que você controla)
    assert result['title'] == 'Test todo'
    assert result['description'] == 'Test Desc'
    assert result['state'] == 'draft'
    assert result['user_id'] == user.id

    # 2. Validação Dinâmica (O que o sistema controla)
    assert result['id'] is not None
    assert result['created_at'] is not None
    assert result['updated_at'] is not None

    # 3. Validação do Relacionamento (Sem testar o usuário inteiro de novo)
    assert result['user']['username'] == user.username
    assert result['user']['email'] == user.email


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
