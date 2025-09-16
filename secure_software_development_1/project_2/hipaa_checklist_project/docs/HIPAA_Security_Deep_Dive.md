# HIPAA Security Rule Deep Dive

## Data Entry

- All regulation updates and checklist items are entered via secure, authenticated interfaces:
  - **Django Admin:** Only superusers and staff can add or modify records.
  - **React Frontend:** Users must log in with valid credentials to access protected routes.
- Example:  
  ![Django admin add regulation screenshot](screenshots/admin_add_regulation.png)
- Only authorized users can add or modify sensitive data. Unauthorized attempts are logged and denied.

## Encryption

- Sensitive fields (e.g., regulation descriptions, checklist notes) are encrypted at rest using `django-encrypted-model-fields`.
- Example model field:
  ```python
  description = EncryptedTextField()
  notes = EncryptedCharField(max_length=500, blank=True, null=True)
  ```
- The encryption key is securely managed in the Django settings and loaded from environment variables:
  ```python
  FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')
  ```
- Verification:  
  - Raw database entries for encrypted fields appear as unreadable ciphertext.
  - Example (from SQLite):
    ```
    x02d1b7e8c9a... (encrypted)
    ```
  - ![Database encrypted field screenshot](screenshots/db_encrypted_field.png)

## Audit Logging

- All changes to regulations and checklist items are tracked using `django-auditlog`.
- Example log entry:
  ```
  [2024-06-01 12:35:10] User 'alice' updated ChecklistItem: completed=True, notes changed.
  ```
- Audit logs record who made each change, what was changed, and when.
- Screenshot:
  ![Auditlog entry screenshot](screenshots/auditlog_entry.png)
- This supports HIPAA requirements for accountability and traceability (HIPAA §164.312(b): Audit Controls).

## Access Control

- Only authenticated users can access the system.
- Admin-only data is protected by Django permissions and group-based access control.
- Example Django permission check:
  ```python
  def has_change_permission(self, request, obj=None):
      return request.user.is_superuser or request.user.groups.filter(name='ComplianceAdmin').exists()
  ```
- Unauthorized access attempts are logged and result in a 403 Forbidden response.

## HIPAA Security Rule Mapping

| Control Area      | Implementation Example                                 | HIPAA Reference         |
|-------------------|-------------------------------------------------------|-------------------------|
| Access Control    | Django auth, admin permissions, JWT tokens            | §164.312(a)             |
| Audit Controls    | django-auditlog, log review, evidence collection      | §164.312(b)             |
| Integrity         | Encrypted fields, database backups, change tracking   | §164.312(c)             |
| Transmission Sec. | HTTPS enforced via Nginx and Django settings          | §164.312(e)             |

---

*This document demonstrates how the HIPAA Security Rule is enforced in the HIPAA Checklist project, with a focus on secure data entry, encryption, audit logging, and access control, supported by real-world examples and system outputs.*