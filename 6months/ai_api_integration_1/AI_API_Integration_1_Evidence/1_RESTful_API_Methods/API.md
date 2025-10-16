# API Documentation

## Authentication
- Obtain JWT token:
  - `POST /api/token/` with `{ username, password }`
  - Response: `{ "access": "...", "refresh": "..." }`
- Use `Authorization: Bearer <token>` header for all protected endpoints.

## Endpoints

### Checklist Items
- `GET /api/checklist/` — List checklist items for current user
- `PATCH /api/checklist/<id>/` — Update checklist item (fields: completed, notes, mitigation_steps, etc.)
- Fields: user, regulation_update, completed, notes, admin_notes, mitigation_steps, last_updated, likelihood, impact

### Regulation Updates
- `GET /api/regulations/` — List regulation updates

### Compliance Report
- `GET /api/report/` — Get compliance report for current user

### Audit Log
- `GET /api/auditlog/checklistitem/<id>/` — Get audit log for a checklist item
- `GET /api/auditlog/regulationupdate/<id>/` — Get audit log for a regulation update
- Response: list of entries with timestamp, actor, action, changes, remote_addr

## Example: Get Checklist Items
```
GET /api/checklist/
Authorization: Bearer <token>
```
Response:
```
[
  {
    "id": 1,
    "user": "alice",
    "regulation_update": "HIPAA Security Rule Update",
    "completed": false,
    "notes": "Initial assignment.",
    "mitigation_steps": "Encrypt all PHI at rest.",
    ...
  },
  ...
]
```

## Example: Get Audit Log
```
GET /api/auditlog/checklistitem/1/
Authorization: Bearer <token>
```
Response:
```
[
  {
    "timestamp": "2024-06-01T12:34:56Z",
    "actor": "alice",
    "action": "Update",
    "changes": { "notes": ["old", "new"] },
    "remote_addr": "127.0.0.1"
  },
  ...
]
```