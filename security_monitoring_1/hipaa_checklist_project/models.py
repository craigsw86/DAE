from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields import EncryptedTextField

class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    notes = EncryptedTextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

class RegulationUpdate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    source_url = models.URLField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(default=False) # For admin review
    