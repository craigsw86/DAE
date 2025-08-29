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
    list_display = ('title', 'created_at', 'updated_at', 'checklist_items_count')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20
    date_hierarchy = 'created_at'
    fields = ('title', 'description', 'source_url', 'created_at')
    readonly_fields = ('created_at',)
    
    def checklist_items_count(self, obj):
        return obj.checklistitem_set.count()
    checklist_items_count.short_description = 'Checklist Items'

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation_update', 'completed', 'last_updated', 'likelihood', 'impact', 'mitigation_steps')
    list_filter = ('completed', 'likelihood', 'impact', 'user', 'last_updated')
    search_fields = ('user__username', 'regulation_update__title', 'notes', 'admin_notes', 'mitigation_steps')
    list_per_page = 25
    date_hierarchy = 'last_updated'
    fields = ('user', 'regulation_update', 'completed', 'notes', 'admin_notes', 'mitigation_steps', 'last_updated', 'likelihood', 'impact')
    readonly_fields = ('last_updated',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(RegulationUpdate, RegulationUpdateAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
