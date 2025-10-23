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
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    regulation_update = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE, db_index=True, db_column='regulation_update_id')
    completed = models.BooleanField(default=False, db_index=True)
    notes = EncryptedCharField(max_length=500, blank=True, null=True)
    admin_notes = EncryptedCharField(max_length=500, blank=True, null=True, help_text="Admin/internal comments")
    mitigation_steps = EncryptedTextField(blank=True, null=True, help_text="Describe mitigation steps for this risk.")
    last_updated = models.DateTimeField(auto_now=True, db_index=True)
    likelihood = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1,6)], help_text="Likelihood (1=Low, 5=High)", db_index=True)
    impact = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1,6)], help_text="Impact (1=Low, 5=High)", db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['regulation_update', 'completed']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.regulation_update.title} (L:{self.likelihood}, I:{self.impact}) | Mitigation: {self.mitigation_steps[:20] if self.mitigation_steps else 'None'}"

auditlog.register(RegulationUpdate)
auditlog.register(ChecklistItem)