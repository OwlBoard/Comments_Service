import os
import sys
from typing import AsyncGenerator

import mongomock_motor
import pytest_asyncio
from beanie import PydanticObjectId, init_beanie
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from src.models import Comment


# --- Base de datos en memoria con mongomock ---
@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_test_database():
    """
    Inicializa la base de datos en memoria (mongomock) para los tests.
    """
    client = mongomock_motor.AsyncMongoMockClient()
    db = client["test_db"]

    await init_beanie(database=db, document_models=[Comment])

    yield



@pytest_asyncio.fixture(autouse=True)
async def clear_collections() -> AsyncGenerator[None, None]:
    """Limpia la colección de comentarios después de cada test."""
    yield
    await Comment.delete_all()


# --- Cliente HTTP para pruebas ---
@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def created_comment() -> Comment:
    """Crea un comentario de prueba en la base de datos y devuelve el objeto."""
    comment = Comment(
        dashboard_id=PydanticObjectId(),
        user_id=PydanticObjectId(),
        content="Comentario original",
        coordinates=[0, 0],
    )
    await comment.insert()
    return comment
