# Procedure: Enabling Field-Level Encryption in Django

## Purpose
To ensure sensitive data is protected at rest by enabling field-level encryption in the HIPAA Checklist project.

## Steps
1. Install the `django-encrypted-model-fields` package.
2. Import `EncryptedCharField` and `EncryptedTextField` in your models.
3. Update sensitive model fields to use encrypted types.
4. Set a secure `FIELD_ENCRYPTION_KEY` in your Django settings.
5. Run migrations to apply changes.
6. Test by creating and retrieving encrypted data via the Django shell.