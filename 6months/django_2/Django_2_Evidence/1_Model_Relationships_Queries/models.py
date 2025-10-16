# These models use encrypted fields to protect sensitive data at rest and are registered with auditlog for change tracking.
# This supports Zero Trust and Defense in Depth security principles.
#
# Audit logging is enabled for all sensitive models.

from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
from auditlog.registry import auditlog

class RegulationUpdate(models.Model):
    """
    Model representing HIPAA regulation updates and requirements.
    
    This model stores regulation information with encrypted description fields
    to protect sensitive regulatory content. Each regulation can have multiple
    checklist items associated with it.
    
    Fields:
    - title: Human-readable title of the regulation
    - description: Encrypted text containing the full regulation details
    - source_url: Optional URL reference to the regulation source
    - created_at: Timestamp when the regulation was first added
    - updated_at: Timestamp when the regulation was last modified
    """
    title = models.CharField(max_length=255)
    description = EncryptedTextField()
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the regulation update.
        
        Returns:
            str: The title of the regulation for display purposes
        """
        return self.title
    
class ChecklistItem(models.Model):
    """
    Model representing individual checklist items for HIPAA compliance tracking.
    
    This is the core model that tracks user-specific compliance items with
    encrypted fields for sensitive data protection. Each item is associated
    with a regulation and includes risk assessment fields.
    
    Fields:
    - user: Foreign key to the user who owns this checklist item
    - regulation_update: Foreign key to the associated regulation
    - completed: Boolean flag indicating if the item is completed
    - notes: Encrypted user notes about the checklist item
    - admin_notes: Encrypted admin-only notes (not visible to regular users)
    - mitigation_steps: Encrypted text describing risk mitigation steps
    - last_updated: Timestamp of the last modification
    - likelihood: Risk likelihood score (1-5 scale)
    - impact: Risk impact score (1-5 scale)
    """
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
        """
        Meta configuration for the ChecklistItem model.
        
        Defines database indexes for optimized querying:
        - Composite index on user and completed status for user-specific queries
        - Composite index on regulation and completed status for regulation-specific queries
        """
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['regulation_update', 'completed']),
        ]

    def __str__(self):
        """
        String representation of the checklist item.
        
        Returns:
            str: Formatted string showing user, regulation, risk scores, and mitigation preview
        """
        return f"{self.user.username} - {self.regulation_update.title} (L:{self.likelihood}, I:{self.impact}) | Mitigation: {self.mitigation_steps[:20] if self.mitigation_steps else 'None'}"

# Register models with audit logging for comprehensive change tracking
# This enables automatic logging of all create, update, and delete operations
# for compliance and security auditing purposes
auditlog.register(RegulationUpdate)
auditlog.register(ChecklistItem)