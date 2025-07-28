from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField
from auditlog.registry import auditlog

class RegulationUpdate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation_update = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    notes = EncryptedCharField(max_length=500, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.regulation_update.title}"
 
auditlog.register(RegulationUpdate)
auditlog.register(ChecklistItem)