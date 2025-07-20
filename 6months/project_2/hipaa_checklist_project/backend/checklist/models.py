from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedTextField
from auditlog.registry import auditlog

class Regulation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    code = models.CharField(max_length=50, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

class UserChecklist(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=Fasle)
    notes = EncryptedTextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

auditlog.register(Regulation)
auditlog.register(UserChecklist)
