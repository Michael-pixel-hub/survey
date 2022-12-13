from django.conf import settings
from django.contrib import admin
from public_model.admin import public_model
from sort_model.admin import order_model

from .models import String, Menu, Channel


@admin.register(String)
class StringAdmin (admin.ModelAdmin):
    """
    Администрирование строковых переменных
    """

    def get_list_display(self, request):
        if request.user.email == settings.AUTH_USER_DEVELOPER or settings.DEBUG:
            return 'name', 'slug', 'category', 'print_value',
        return super(StringAdmin, self).get_list_display(request)

    def get_readonly_fields(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER or settings.DEBUG:
            return ()
        return self.readonly_fields

    def get_actions(self, request):
        if request.user.email == settings.AUTH_USER_DEVELOPER or settings.DEBUG:
            return super(StringAdmin, self).get_actions(request)
        return None

    def has_add_permission(self, request):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    list_display = ('name', 'category', 'print_value',)
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'value', )
        }),
    )
    search_fields = ('name', 'category', 'slug', 'value',)
    list_filter = ('category', )
    readonly_fields = ('name', 'category', 'slug',)


@public_model
@order_model
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'value', )
        }),
    )
    search_fields = ['name', 'value']


@public_model
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):

    list_display = ('name', 'telegram_id', )
    list_display_links = ('name', 'telegram_id', )

    fieldsets = (
        (None, {
            'fields': ('name', 'telegram_id', )
        }),
    )
    search_fields = ['name', 'telegram_id']
