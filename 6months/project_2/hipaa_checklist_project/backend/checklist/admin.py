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
    fields = ('title', 'description', 'source_url', 'created_at')
    readonly_fields = ('created_at',)

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation_update', 'completed', 'last_updated', 'likelihood', 'impact', 'mitigation_steps')
    fields = ('user', 'regulation_update', 'completed', 'notes', 'admin_notes', 'mitigation_steps', 'last_updated', 'likelihood', 'impact')
    readonly_fields = ('last_updated',)

admin.site.register(RegulationUpdate, RegulationUpdateAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
