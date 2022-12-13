from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from public_model.admin import public_model
from sort_model.admin import order_model

from .forms import OrderForm
from .models import String, Menu, User, Report, Task, Order


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


@admin.register(User)
class UserAdmin (admin.ModelAdmin):

    list_display = ('company_name', 'fio', 'phone', 'email', 'is_register', 'is_telegram', 'telegram_username',
                    'telegram_first_name', 'telegram_last_name', 'is_manager')
    list_display_links = ('company_name', 'telegram_username')

    fieldsets = (
        (_('Dates'), {
            'fields': ('date_join', 'is_manager')
        }),
        (_('Personal data'), {
            'fields': ('is_register', 'company_name', 'company_inn', 'fio', 'phone', 'email', )
        }),
        (_('Telegram data'), {
            'fields': ('is_telegram', 'telegram_username', 'telegram_first_name', 'telegram_last_name',
                       'telegram_language_code', 'telegram_id',)
        }),
    )
    readonly_fields = ('date_join', )
    search_fields = ('telegram_id', 'telegram_language_code', 'telegram_last_name', 'telegram_first_name',
                     'telegram_username', 'company_name', 'company_inn', 'fio', 'phone', 'email')
    date_hierarchy = 'date_join'
    list_filter = ('is_register', 'is_manager')


@admin.register(Report)
class ReportAdmin (admin.ModelAdmin):

    list_display = ('date_upload', 'file', 'user', 'description')
    list_display_links = ('date_upload', 'file')

    fieldsets = (
        (_('Report'), {
            'fields': ('date_upload', 'file', 'description')
        }),
        (_('For user'), {
            'fields': ('user', )
        }),
    )
    readonly_fields = ('date_upload', )
    search_fields = ('file', 'description', 'user__telegram_username', 'user__company_name', 'user__company_inn',
                     'user__fio', 'user__phone', 'user__email')
    date_hierarchy = 'date_upload'
    raw_id_fields = ['user']
    list_select_related = ('user', )


@public_model
@order_model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ('name', 'type', 'price', 'is_offered', 'author', )
    list_display_links = ('name', )

    fieldsets = (
        (_('Task'), {
            'fields': ('name', 'type', 'price', 'description', )
        }),
        (_('User offered'), {
            'fields': ('is_offered', 'author', 'date_offered',)
        }),
    )
    raw_id_fields = ['author']
    search_fields = ['name', 'type', 'description', 'author__telegram_username', 'author__company_name',
                     'author__company_inn', 'author__fio', 'author__phone', 'author__email']
    list_select_related = ('author',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    form = OrderForm

    list_display = ('date_create', 'user', 'task', 'date_start', 'date_end', 'status', )
    list_display_links = ('date_create', 'user', 'task', )

    fieldsets = (
        (_('Order'), {
            'fields': ('user', 'task', ('date_start', 'date_end'), 'status', )
        }),
        (_('Dates'), {
            'fields': ('date_create', 'date_finish',)
        }),
        (_('Where execute'), {
            'fields': ('clients', 'stores', 'regions')
        }),
        (_('Periodicity'), {
            'fields': ('is_once', 'per_week', 'days_of_week',)
        }),
        (_('Is moderate'), {
            'classes': ('collapse',),
            'fields': ('is_moderate', 'moderate_description')
        }),
        (_('Is not moderate'), {
            'classes': ('collapse',),
            'fields': ('is_not_moderate', 'not_moderate_description')
        }),
        (_('Is invoice'), {
            'classes': ('collapse',),
            'fields': ('is_invoice', 'invoice_file', 'invoice_description')
        }),
        (_('Is finished'), {
            'classes': ('collapse',),
            'fields': ('is_finished', 'finished_description')
        }),
    )
    raw_id_fields = ['user']
    search_fields = ['task__name', 'user__telegram_username', 'user__company_name',
                     'user__company_inn', 'user__fio', 'user__phone', 'user__email']
    list_select_related = ('user', 'task')
    date_hierarchy = 'date_create'
    readonly_fields = ['date_create']
    list_filter = ('status',)
