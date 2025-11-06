import pytest
from httpx import AsyncClient
from fastapi import status
from beanie import PydanticObjectId

from app import app
from src.models import Comment

pytestmark = pytest.mark.asyncio


async def test_create_comment(async_client: AsyncClient):
    """Prueba la creación exitosa de un comentario."""
    dashboard_id = "615d08a7a8b2b2a7c2f8a8b3"
    user_id = "615d08a7a8b2b2a7c2f8a8b4"
    comment_data = {
        "content": "Este es un nuevo comentario de prueba.",
        "coordinates": "10.5,20.2",
        "user_name": "test_user"
    }

    response = await async_client.post(
        f"/comments/dashboards/{dashboard_id}/users/{user_id}/comments",
        json=comment_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["content"] == comment_data["content"]
    assert data["dashboard_id"] == dashboard_id
    assert data["user_id"] == user_id
    assert data["coordinates"] == [10.5, 20.2]
    assert "_id" in data

    comment_in_db = await Comment.get(data["_id"])
    assert comment_in_db is not None
    assert comment_in_db.content == comment_data["content"]


async def test_get_comment(async_client: AsyncClient, created_comment: Comment):
    """Prueba obtener un comentario existente por su ID."""
    response = await async_client.get(f"/comments/{created_comment.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["_id"] == str(created_comment.id)
    assert data["content"] == created_comment.content


async def test_get_comment_not_found(async_client: AsyncClient):
    """Prueba que se obtiene un 404 al buscar un comentario inexistente."""
    non_existent_id = PydanticObjectId()
    response = await async_client.get(f"/comments/{non_existent_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_all_comments_from_dashboard(async_client: AsyncClient, created_comment: Comment):
    """Prueba obtener todos los comentarios de un tablero."""
    # Crear otro comentario en el mismo tablero
    await Comment(
        dashboard_id=created_comment.dashboard_id,
        user_id=PydanticObjectId(),
        content="Otro comentario",
        coordinates=[1, 1]
    ).insert()

    response = await async_client.get(f"/comments/dashboards/{created_comment.dashboard_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert {item["content"] for item in data} == {"Comentario original", "Otro comentario"}


async def test_get_all_comments_from_empty_dashboard(async_client: AsyncClient):
    """Prueba obtener comentarios de un tablero que no tiene ninguno."""
    dashboard_id = PydanticObjectId()
    response = await async_client.get(f"/comments/dashboards/{dashboard_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_update_comment(async_client: AsyncClient, created_comment: Comment):
    """Prueba actualizar el contenido de un comentario existente."""
    update_data = {"content": "Contenido actualizado."}

    response = await async_client.put(f"/comments/{created_comment.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["content"] == update_data["content"]
    assert data["_id"] == str(created_comment.id)
    # Verifica que la fecha de actualización ha cambiado
    assert data["updated_at"] > data["created_at"]

    comment_in_db = await Comment.get(created_comment.id)
    assert comment_in_db.content == update_data["content"]


async def test_update_comment_not_found(async_client: AsyncClient):
    """Prueba que se obtiene un 404 al intentar actualizar un comentario inexistente."""
    non_existent_id = PydanticObjectId()
    update_data = {"content": "No debería funcionar."}
    response = await async_client.put(f"/comments/{non_existent_id}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_comment_no_data(async_client: AsyncClient, created_comment: Comment):
    """Prueba que se obtiene un 400 si no se envían datos para actualizar."""
    response = await async_client.put(f"/comments/{created_comment.id}", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_delete_comment(async_client: AsyncClient, created_comment: Comment):
    """Prueba eliminar un comentario existente."""
    response = await async_client.delete(f"/comments/{created_comment.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    comment_in_db = await Comment.get(created_comment.id)
    assert comment_in_db is None


async def test_delete_comment_not_found(async_client: AsyncClient):
    """Prueba que se obtiene un 404 al intentar eliminar un comentario inexistente."""
    non_existent_id = PydanticObjectId()
    response = await async_client.delete(f"/comments/{non_existent_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

