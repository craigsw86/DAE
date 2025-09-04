from django import forms
from .models import ChecklistItem

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['regulation_update', 'completed', 'notes']
        labels = {
            'regulation_update': 'Regulation',
            'completed': 'Mark as Completed',
            'notes': 'Notes (optional)',
        }
        help_texts = {
            'regulation_update': 'Select the regulation this checklist item relates to.',
            'completed': 'Check if this item is complete.',
            'notes': 'Add any relevant notes or context for this item.',
        }
        widgets = {
            'regulation_update': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a regulation',
                'required': 'required',
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notes (optional)',
                'rows': 3,
            }),
        }
