from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedTextField
from auditlog.registry import auditlog

class RegulationUpdate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_url = models.URLField()
    pub_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation_update = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    notes = EncryptedTextField(blank=True)  # HIPAA-compliant encryption
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'regulation_update']

auditlog.register(RegulationUpdate)  # Log changes for governance
auditlog.register(ChecklistItem)