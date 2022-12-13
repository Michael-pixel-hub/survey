from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Notification


@admin.register(Notification)
class NotificationAdmin (admin.ModelAdmin):

    def short_message(self, obj):
        s = str(obj.message)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    short_message.short_description = _('Message')

    list_display = ('date_create', 'user', 'category', 'title', 'short_message', 'is_sent', )
    list_display_links = ('date_create', 'user', )

    fieldsets = (
        (None, {
            'fields': ('date_create', 'user', 'category', 'title', 'message',)
        }),
        (_('Result'), {
            'fields': ('result',)
        }),
        (_('Flags'), {
            'fields': ('is_sent',)
        }),
    )
    date_hierarchy = 'date_create'
    readonly_fields = ('date_create', )
    list_select_related = ('user',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__telegram_id', 'user__phone',
                     'user__name', 'user__surname', 'user__email', 'title', 'message']
    raw_id_fields = ['user']
    list_filter = ('category', )
