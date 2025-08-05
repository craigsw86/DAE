# API Testing with Postman

This guide explains how to test your Django REST API endpoints using Postman, including authentication, CRUD operations, and the raw SQL user filtering endpoint.

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
      "notes": "Raw SQL note",
      "last_updated": "2024-06-01T12:00:00Z",
      "regulation_update_id": 1
    },
    ...
  ]
  ```

---

## 4. Tips
- Always include the `Authorization: Bearer <access_token>` header for protected endpoints.
- Use the `/api/token/refresh/` endpoint to refresh your access token if it expires.
- You can use the Postman "Pre-request Script" or "Environment Variables" to automate token handling if desired.

---

## 5. Example Postman Collection
You can import these endpoints into Postman and save your token as an environment variable for convenience.