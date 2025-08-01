# HIPAA Checklist API Documentation

## Authentication
- All API endpoints require JWT authentication.
- Obtain a token via POST `/api/token/` with username and password.
- Include the token in the `Authorization` header:
  ```
  Authorization: Bearer <access_token>
  ```
- All endpoints require HTTPS for secure transmission.

## Endpoints

### Checklist Items
- `GET /api/checklist/` — List checklist items for the authenticated user
- `POST /api/checklist/` — Create a new checklist item
- `PATCH /api/checklist/{id}/` — Update a checklist item
- `DELETE /api/checklist/{id}/` — Delete a checklist item

#### Sample Checklist Item Response
```json
{
  "id": 1,
  "user": "alice",
  "regulation_update": "HIPAA Security Rule",
  "completed": true,
  "notes": "Reviewed and compliant.",
  "last_updated": "2024-06-01T12:34:56Z"
}
```

### Regulation Updates
- `GET /api/regulations/` — List all regulation updates
- `POST /api/regulations/` — Create a new regulation update (admin only)

#### Sample Regulation Update Response
```json
{
  "id": 1,
  "title": "HIPAA Security Rule",
  "description": "Safeguards for ePHI...",
  "source_url": "https://www.hhs.gov/hipaa/for-professionals/security/index.html",
  "created_at": "2024-06-01T12:00:00Z",
  "updated_at": "2024-06-01T12:00:00Z"
}
```

### Compliance Report
- `GET /api/report/` — Get compliance stats for the authenticated user

#### Sample Request
```
GET /api/report/
Authorization: Bearer <access_token>
```

#### Sample Response
```json
{
  "user": "alice",
  "total_items": 10,
  "completed_items": 7,
  "completion_percentage": 70.0
}
```

## Error Handling
- `401 Unauthorized`: Returned if the JWT token is missing or invalid.
- `403 Forbidden` or `404 Not Found`: Returned if a user tries to access another user’s data.

## Audit Logging
- All changes to checklist items and regulations are tracked using django-auditlog.
- Audit logs record who made each change, what was changed, and when.

## Security
- All endpoints require HTTPS and JWT authentication.
- Sensitive actions are logged for audit and compliance.

## Interactive API
- You can explore and test the API interactively at `/api/` using the DRF browsable API (when DEBUG is enabled).

For more details, see [Project README](../README.md).