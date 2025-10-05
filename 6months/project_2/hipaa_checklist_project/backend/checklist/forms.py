from django import forms
from .models import ChecklistItem, RegulationUpdate

class ChecklistItemForm(forms.ModelForm):
    """
    Django form for creating and editing checklist items.
    
    This form provides a user-friendly interface for managing checklist items
    with proper field validation, help text, and user permission handling.
    Includes risk assessment fields and encrypted note fields.
    """
    
    # Regulation selection field with dropdown
    regulation_update = forms.ModelChoiceField(
        queryset=RegulationUpdate.objects.all(),
        empty_label="Select a Regulation",
        label="Associated Regulation",
        help_text="Choose the regulation this checklist item pertains to.",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Completion status checkbox
    completed = forms.BooleanField(
        required=False,
        label="Mark as Completed",
        help_text="Check if this item has been completed.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Risk likelihood assessment (1-5 scale)
    likelihood = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1,6)],
        label="Likelihood (1=Low, 5=High)",
        help_text="How likely is this risk?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Risk impact assessment (1-5 scale)
    impact = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1,6)],
        label="Impact (1=Low, 5=High)",
        help_text="What is the impact if this risk occurs?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # User notes field (encrypted)
    notes = forms.CharField(
        required=False,
        label="Notes/Comments",
        help_text="Add any relevant notes or observations.",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter notes here...', 'class': 'form-control'})
    )
    
    # Admin notes field (encrypted, admin-only)
    admin_notes = forms.CharField(
        required=False,
        label="Admin Notes",
        help_text="Internal/admin comments (visible to admins only)",
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Admin/internal notes...', 'class': 'form-control'})
    )

    class Meta:
        """
        Meta configuration for the ChecklistItemForm.
        
        Specifies the model and fields to include in the form.
        """
        model = ChecklistItem
        fields = ['regulation_update', 'completed', 'likelihood', 'impact', 'notes', 'admin_notes']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with user-specific field visibility.
        
        Removes admin_notes field for non-staff users to maintain
        proper access control and data security.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments (including 'user')
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Hide admin notes field for regular users
        if user and not (user.is_staff or user.is_superuser):
            self.fields.pop('admin_notes', None)
