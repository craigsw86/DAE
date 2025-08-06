# API Testing with Postman

This guide explains how to test your Django REST API endpoints using Postman, including authentication, CRUD operations, and the raw SQL user filtering endpoint.

---

## Quick Start
1. **Start your Django server:**
   ```sh
   python manage.py runserver
   ```
2. **Open Postman (desktop or web).**
3. **Import the provided Postman collection:**
   - File: `docs/Postman_Collection.json`
   - Click "Import" in Postman and select the file.
4. **Set up environment variables:**
   - Click the "Environment" dropdown (top right), create/select an environment.
   - Add variables: `base_url` (`http://localhost:8000`), `username`, `password`, `access_token` (leave blank initially).
5. **Obtain your JWT token:**
   - Use the "Auth - Obtain Token" request.
   - Enter your username and password in the body or environment.
   - Click "Send" and copy the `access` token to your environment.
6. **Test other endpoints using the token.**

---

## 1. Authentication (Obtain JWT Token)

- **Endpoint:** `POST /api/token/`
- **URL:** `http://localhost:8000/api/token/`
- **Body:** (raw, JSON)
  ```json
  {
    "username": "yourusername",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
  ```
- **Instructions:**
  - Copy the `access` token for use in the `Authorization` header for all subsequent requests.

---

## 2. ChecklistItem CRUD Operations

### a. List All Checklist Items
- **Endpoint:** `GET /api/checklist/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "user": "username",
      "regulation_update": "Regulation Title",
      "completed": false,
      "notes": "Some notes",
      "last_updated": "2024-06-01T12:00:00Z"
    },
    ...
  ]
  ```

### b. Create a Checklist Item
- **Endpoint:** `POST /api/checklist/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "user": 1,
    "regulation_update": 1,
    "completed": false,
    "notes": "Initial assignment."
  }
  ```
- **Response:** Checklist item object (as above)

### c. Update a Checklist Item
- **Endpoint:** `PUT /api/checklist/{id}/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
  - `Content-Type: application/json`
- **Body:** (all fields required)
- **Response:** Updated checklist item object

### d. Partial Update (PATCH)
- **Endpoint:** `PATCH /api/checklist/{id}/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
  - `Content-Type: application/json`
- **Body:** (only fields to update)
- **Response:** Updated checklist item object

### e. Delete a Checklist Item
- **Endpoint:** `DELETE /api/checklist/{id}/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Response:** `204 No Content`

---

## 3. Raw SQL User Filtering Endpoint

### a. Get Checklist Items for Current User (Raw SQL)
- **Endpoint:** `GET /api/checklist/my_items_raw/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "completed": false,
      "notes": "<encrypted>",
      "last_updated": "2024-06-01T12:00:00Z",
      "regulation_update_id": 1
    },
    ...
  ]
  ```
  - Note: The `notes` field is encrypted at rest and will not match the plaintext value.

---

## 4. Using Environment Variables in Postman
- Store your `base_url`, `username`, `password`, and `access_token` as environment variables for easy reuse.
- Use `{{access_token}}` in the Authorization header: `Bearer {{access_token}}`.
- You can automate setting the token with a "Test" script in the Auth request:
  ```js
  // In the Tests tab of the Auth request
  if (pm.response.code === 200) {
    var json = pm.response.json();
    pm.environment.set("access_token", json.access);
  }
  ```

---

## 5. Troubleshooting
- **401 Unauthorized:** Check your username/password, token, and that the server is running.
- **404 Not Found:** Check the endpoint URL and that the server is running.
- **400 Bad Request:** Check your request body for correct JSON and required fields.
- **Connection Refused:** Make sure the Django server is running at `http://localhost:8000/`.

---

## 6. Alternative: Python Script for Token Retrieval
If you prefer not to use Postman, you can use the provided Python script:
```python
import requests
url = "http://localhost:8000/api/token/"
data = {"username": "yourusername", "password": "yourpassword"}
response = requests.post(url, json=data)
print(response.json())
```

---

## 7. Example Postman Collection
You can import these endpoints into Postman and save your token as an environment variable for convenience.

---

*For more details, see [API.md](API.md) and [README.md](../README.md).*