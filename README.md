# Comments_Service

This service, built with FastAPI and Beanie (MongoDB), manages all comments within the OwlBoard whiteboards.

The comments service will be available at `http://localhost:8001`.

## 📚 API Endpoints

The available service endpoints are detailed below.

---

### 1. Create a new comment

Creates a new comment associated with a user and a board, specifying its content and coordinates.

*   **Endpoint:** `POST /dashboards/{dashboard_id}/users/{user_id}/comments`
*   **Status Code:** `201 CREATED`

#### Path Parameters

| Parameter      | Type               | Description                             |
| :------------- | :----------------- | :-------------------------------------- |
| `dashboard_id` | `PydanticObjectId` | The ID of the board where the comment is created. |
| `user_id`      | `PydanticObjectId` | The ID of the user creating the comment. |

#### Request Body

```json
{
  "content": "This is a new comment.",
  "coordinates": "150.5,320.0"
}
```

#### Respuesta Exitosa (Success Response)

```json
{
  "id": "650c1f2a1b2c3d4e5f6a7b8c",
  "dashboard_id": "6507f1f130ade8d4e9bf7b5a",
  "user_id": "6507f1f130ade8d4e9bf7b5b",
  "content": "Este es un nuevo comentario.",
  "coordinates": [150.5, 320.0],
  "created_at": "2023-09-21T12:00:00Z",
  "updated_at": "2023-09-21T12:00:00Z"
}
```

---

### 2. Obtener todos los comentarios de un tablero

*   **Endpoint:** `GET /dashboards/{dashboard_id}`
*   **Descripción:** Devuelve una lista con todos los comentarios que pertenecen a un tablero específico.

---

### 3. Obtener un comentario por ID

*   **Endpoint:** `GET /{comment_id}`
*   **Descripción:** Devuelve un comentario específico basado en su ID.
*   **Errores:** `404 NOT FOUND` si el comentario no existe.

---

### 4. Actualizar un comentario

*   **Endpoint:** `PUT /{comment_id}`
*   **Descripción:** Actualiza el contenido y/o las coordenadas de un comentario existente.

#### Cuerpo de la Solicitud (Request Body)

Puedes enviar uno o más campos para actualizar.

```json
{
  "content": "Este es el contenido actualizado.",
  "coordinates": [200.0, 450.5]
}
```

*   **Errores:** `404 NOT FOUND` si el comentario no existe.

---

### 5. Eliminar un comentario

*   **Endpoint:** `DELETE /{comment_id}`
*   **Descripción:** Elimina un comentario de forma permanente usando su ID.
*   **Respuesta:** `{"message": "Comentario eliminado"}`
*   **Errores:** `404 NOT FOUND` si el comentario no existe.
