# Procedure: Enabling Field-Level Encryption in Django

## Purpose
To ensure sensitive data is protected at rest by enabling field-level encryption in the HIPAA Checklist project.

## Scope
This procedure applies to all Django models containing PHI/PII or other sensitive data.

## Roles and Responsibilities

| Role         | Responsibilities                                 |
|--------------|--------------------------------------------------|
| Developer    | Implements and tests encryption in models        |
| System Admin | Manages encryption keys, applies migrations      |
| Security Officer | Verifies encryption and reviews compliance   |

---

## Step-by-Step Procedure

1. **Install the Encryption Package**
   - Run:
     ```
     pip install django-encrypted-model-fields
     ```
   - Responsible: Developer

2. **Import Encrypted Field Types**
   - In your models file:
     ```python
     from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
     ```
   - Responsible: Developer

3. **Update Model Fields**
   - Change sensitive fields to use encrypted types:
     ```python
     description = EncryptedTextField()
     notes = EncryptedCharField(max_length=500, blank=True, null=True)
     ```
   - Responsible: Developer

4. **Set the Encryption Key**
   - In `settings.py`:
     ```python
     import os
     FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')
     ```
   - Generate a key:
     ```
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```
   - Store the key securely as an environment variable.
   - Responsible: System Admin

5. **Run Migrations**
   - Apply changes to the database:
     ```
     python manage.py makemigrations
     python manage.py migrate
     ```
   - Responsible: System Admin

6. **Test Encryption**
   - In Django shell:
     ```
     python manage.py shell
     >>> from checklist.models import RegulationUpdate
     >>> ru = RegulationUpdate.objects.create(title='Test', description='Sensitive info')
     >>> RegulationUpdate.objects.get(id=ru.id).description
     'Sensitive info'
     ```
   - Verify in the database that the field is stored as unreadable ciphertext.
   - Responsible: Developer

7. **Evidence**
   - Attach a screenshot of the encrypted field in the database.
   - Example:
     ![Encrypted field screenshot](screenshots/db_encrypted_field.png)

---

## Troubleshooting

- **Error: FIELD_ENCRYPTION_KEY defined incorrectly**
  - Ensure the key is 44 characters, base64-encoded, and set as an environment variable.
- **Data not encrypted in DB**
  - Confirm the model field uses `EncryptedCharField` or `EncryptedTextField`.

---

*This procedure is reviewed annually and after any major change to encryption libraries or project requirements.*