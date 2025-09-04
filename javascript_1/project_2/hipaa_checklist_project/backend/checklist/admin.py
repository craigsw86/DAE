from django.contrib import admin
from .models import RegulationUpdate, ChecklistItem
from django import forms

class RegulationUpdateAdminForm(forms.ModelForm):
    class Meta:
        model = RegulationUpdate
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        }
        help_texts = {
            'description': 'Paste the regulation text here (e.g., from HHS email).',
        }

class RegulationUpdateAdmin(admin.ModelAdmin):
    form = RegulationUpdateAdminForm
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation_update', 'completed', 'last_updated')
    list_filter = ('completed', 'regulation_update')
    search_fields = ('user__username', 'regulation_update__title', 'notes')

admin.site.register(RegulationUpdate, RegulationUpdateAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
