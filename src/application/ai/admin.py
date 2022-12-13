from django.contrib import admin

from .models import AIProject


@admin.register(AIProject)
class AIProjectAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_default', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'is_default', )
        }),
    )
    search_fields = ['name']
    list_filter = ('is_default', )
