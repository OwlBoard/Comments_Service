from fastapi import APIRouter, HTTPException, status, Response, Query, Depends
from beanie import PydanticObjectId 
from src import schemas
from src.models import Comment
from typing import List
from datetime import datetime, timezone

router = APIRouter()

async def parse_coordinates(
    coordinates: str = Query(
        ...,
        description="Coordenadas 'x,y' donde se ubicará el comentario.",
        example="150.5,320.0",
        pattern=r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$"
    )
) -> List[float]:
    try:
        coords_list = [float(c.strip()) for c in coordinates.split(',')]
        if len(coords_list) != 2:
            raise ValueError("Las coordenadas deben tener dos valores (x,y).")
        return coords_list
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de coordenadas inválido: {e}")

# POST Crea un nuevo comentario en un tablero.
@router.post(
    "/dashboards/{dashboard_id}/users/{user_id}/comments",
    response_model=schemas.CommentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo comentario",
    description="Crea un nuevo comentario asociado a un usuario y un tablero, especificando su contenido y coordenadas."
)
async def create_comment(
    dashboard_id: PydanticObjectId,
    user_id: PydanticObjectId,
    comment_in: schemas.CommentCreate,
    coords_list: List[float] = Depends(parse_coordinates)
):
    new_comment = Comment(
        **comment_in.model_dump(),
        dashboard_id=dashboard_id,
        user_id=user_id,
        coordinates=coords_list
    )
    await new_comment.insert()
    return new_comment

# GET Obtener comentario
@router.get(
    "/{comment_id}",
    response_model=schemas.CommentOut,
    summary="Obtener un comentario por su ID"
)
async def get_comment(comment_id: PydanticObjectId):
    comment = await Comment.get(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
    return comment

# GET Obtiene todos los comentarios de un tablero.
@router.get(
    "/dashboards/{dashboard_id}",
    response_model=List[schemas.CommentOut],
    summary="Obtener todos los comentarios de un tablero"
)
async def get_all_comments_from_dashboard(dashboard_id: PydanticObjectId):
    comments = await Comment.find(
        Comment.dashboard_id == dashboard_id
    ).to_list()
    return comments

# PUT Actualiza un comentario específico.
@router.put(
    "/{comment_id}",
    response_model=schemas.CommentOut,
    summary="Actualizar un comentario"
)
async def update_comment(comment_id: PydanticObjectId, comment_update: schemas.CommentUpdate):
    comment = await Comment.get(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    update_data = comment_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se enviaron datos")

    for key, value in update_data.items():
        setattr(comment, key, value)
    comment.updated_at = datetime.now(timezone.utc)

    await comment.save()
    return comment

# DELETE Elimina un comentario específico.
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un comentario")
async def delete_comment(comment_id: PydanticObjectId):
    comment = await Comment.get(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    await comment.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
