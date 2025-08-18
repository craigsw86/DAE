from django import forms
from .models import ChecklistItem, RegulationUpdate

class ChecklistItemForm(forms.ModelForm):
    regulation_update = forms.ModelChoiceField(
        queryset=RegulationUpdate.objects.all(),
        empty_label="Select a Regulation",
        label="Associated Regulation",
        help_text="Choose the regulation this checklist item pertains to.",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    completed = forms.BooleanField(
        required=False,
        label="Mark as Completed",
        help_text="Check if this item has been completed.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    likelihood = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1,6)],
        label="Likelihood (1=Low, 5=High)",
        help_text="How likely is this risk?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    impact = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1,6)],
        label="Impact (1=Low, 5=High)",
        help_text="What is the impact if this risk occurs?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        label="Notes/Comments",
        help_text="Add any relevant notes or observations.",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter notes here...', 'class': 'form-control'})
    )
    admin_notes = forms.CharField(
        required=False,
        label="Admin Notes",
        help_text="Internal/admin comments (visible to admins only)",
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Admin/internal notes...', 'class': 'form-control'})
    )

    class Meta:
        model = ChecklistItem
        fields = ['regulation_update', 'completed', 'likelihood', 'impact', 'notes', 'admin_notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not (user.is_staff or user.is_superuser):
            self.fields.pop('admin_notes', None)
