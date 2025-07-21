from django.contrib import admin
from .models import RegulationUpdate, ChecklistItem

@admin.register(RegulationUpdate)
class RegulationUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'created_at')
    search_fields = ('title', 'description')
    # Governance: Admins manually add from HHS emails; audit logs track entries

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation_update', 'completed', 'last_updated')
    list_filter = ('user', 'completed')
    # Restrict views to user-specific data for compliance