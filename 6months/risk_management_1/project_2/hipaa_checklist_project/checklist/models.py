
from django.db import models
from encrypted_model_fields.fields import EncryptedTextField

class RegulationUpdate(models.Model):
    title = models.CharField(max_length=255)
    description = EncryptedTextField()
    source_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ChecklistItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    regulation = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    notes = EncryptedTextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.regulation.title}"
