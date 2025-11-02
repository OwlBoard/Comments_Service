# Comments_Service

This service, built with FastAPI and Beanie (MongoDB), manages all comments within the OwlBoard whiteboards.

---
 
## 📚 API Endpoints
 
The available service endpoints are detailed below.
 
---

### 1. Create a new comment

Creates a new comment associated with a user and a board, specifying its content and coordinates.

- **Endpoint:** `POST /dashboards/{dashboard_id}/users/{user_id}/comments`  
- **Status Code:** `201 CREATED`

#### Path Parameters

| Parameter      | Type               | Description                                    |
| :------------- | :----------------- | :--------------------------------------------- |
| `dashboard_id` | `PydanticObjectId` | The ID of the board where the comment is created. |
| `user_id`      | `PydanticObjectId` | The ID of the user creating the comment.          |

#### Request Body

```json
{
  "content": "This is a new comment.",
  "coordinates": "150.5,320.0"
}
```

#### Success Response

```json
{
  "content": "Gran dibujo",
  "_id": "68dca9b72cbdae9d5f189556",
  "dashboard_id": "5eb7cf5a86d9755df3a6c593",
  "user_id": "5eb7cf5a86d9755df3a6c593",
  "coordinates": [
    150.5,
    320
  ],
  "created_at": "2025-10-01T04:10:31.732304Z",
  "updated_at": "2025-10-01T04:10:31.732310Z"
}
```

### 2. Get all comments from a board

*   **Endpoint:** `GET /dashboards/{dashboard_id}`
*   **Description:** Returns a list of all comments belonging to a specific board.

#### Path Parameters

| Parameter      | Type               | Description                               |
| :------------- | :----------------- | :---------------------------------------- |
| `dashboard_id` | `PydanticObjectId` | The ID of the board to get comments from. |

#### Success Response (`200 OK`)

Returns a JSON array of comment objects. If there are no comments, it returns an empty array `[]`.

### 3. Get a comment by ID

*   **Endpoint:** `GET /{comment_id}`
*   **Description:** Returns a specific comment based on its ID.
*   **Errors:** `404 NOT FOUND` if the comment does not exist.

#### Success Response

```json
{
  "content": "Gran dibujo",
  "_id": "68dca9b72cbdae9d5f189556",
  "dashboard_id": "5eb7cf5a86d9755df3a6c593",
  "user_id": "5eb7cf5a86d9755df3a6c593",
  "coordinates": [
    150.5,
    320
  ],
  "created_at": "2025-10-01T04:10:31.732000",
  "updated_at": "2025-10-01T04:10:31.732000"
}
```

### 4. Update a comment by ID

- **Endpoint:** `PUT /{comment_id}`
- **Description:** Updates the content of an existing comment identified by its ID.
- **Errors:**
  - `404 NOT FOUND` if the comment does not exist
  - `400 BAD REQUEST` if no data is sent to update

#### Update Parameters

```json
{
  "content": "Updated comment content",
  "coordinates": "160.5,330.0"
}
```

### 5. Update a comment by text

- **Endpoint:** `PUT /update/{comment_text}`
- **Description:** Updates the first comment that matches the exact content provided.
- **Errors:**
  - `404 NOT FOUND` if no comment matches the text
  - `400 BAD REQUEST` if no data is sent to update

#### Request Format

Same structure as update by ID endpoint.

### 6. Delete a comment by ID

- **Endpoint:** `DELETE /{comment_id}`
- **Description:** Permanently deletes a comment using its ID.
- **Success Response (`200 OK`):** `{"message": "Comentario eliminado"}`
- **Errors:** `404 NOT FOUND` if the comment does not exist.

### 7. Delete a comment by text

- **Endpoint:** `DELETE /text/{comment_text}`
- **Description:** Permanently deletes the first comment that matches the exact content provided.
- **Success Response (`200 OK`):** `{"message": "Comentario eliminado"}`
- **Errors:** `404 NOT FOUND` if no comment matches the text.
