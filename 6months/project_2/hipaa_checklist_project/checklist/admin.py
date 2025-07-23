```
from django.contrib import admin
from .models import RegulationUpdate, ChecklistItem

@admin.register(RegulationUpdate)
class RegulationUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulation', 'completed', 'updated_at')
    list_filter = ('completed', 'user')
    search_fields = ('regulation__title', 'notes')
```