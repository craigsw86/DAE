# These models use encrypted fields to protect sensitive data at rest and are registered with auditlog for change tracking.
# This supports Zero Trust and Defense in Depth security principles.
#
# Audit logging is enabled for all sensitive models.

from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
from auditlog.registry import auditlog

class RegulationUpdate(models.Model):
    title = models.CharField(max_length=255)
    description = EncryptedTextField()
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation_update = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    notes = EncryptedCharField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.regulation_update.title}"

auditlog.register(RegulationUpdate)
auditlog.register(ChecklistItem)