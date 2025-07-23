from django.contrib import admin
from .models import RegulationUpdate, ChecklistItem
from encrypted_model_fields.fields import EncryptedTextField  # If using for notes

class RegulationUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'source_url', 'pub_date', 'reviewed')
    search_fields = ('title', 'description')
    list_filter = ('reviewed', 'pub_date')
    formfield_overrides = {
        # Add custom help text for fields if needed
    }
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'source_url', 'pub_date', 'reviewed')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['description'].help_text = "Enter the regulation details here. This will be visible to users."
        return form

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation_update', 'completed', 'last_updated')
    search_fields = ('user__username', 'regulation_update__title')
    list_filter = ('completed', 'last_updated')
    raw_id_fields = ('regulation_update',)  # For easier selection if many updates
    formfield_overrides = {
        EncryptedTextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 5})},
    }
    fieldsets = (
        (None, {
            'fields': ('user', 'regulation_update', 'completed', 'notes', 'last_updated')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['notes'].help_text = "Add encrypted notes here for HIPAA compliance. These are stored securely."
        return form

admin.site.register(RegulationUpdate, RegulationUpdateAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)