from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sort_model.admin import order_model_inline

from .models import Department, DepartmentMenuItem, Program, Store, ProgramPeriod


@order_model_inline
class DepartmentMenuItemInlineTabularAdmin (admin.StackedInline):

    model = DepartmentMenuItem
    fields = ('name', 'value', 'action', 'file', 'url', 'is_public', )
    extra = 0


@admin.register(Department)
class DepartmentAdmin (admin.ModelAdmin):

    list_display = ('name', 'sys_name', )
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name',)
        }),
    )
    search_fields = ('name', 'sys_name', )
    inlines = [DepartmentMenuItemInlineTabularAdmin]


class ProgramPeriodInlineTabularAdmin (admin.TabularInline):

    model = ProgramPeriod
    fields = ('date_start', 'date_end', 'current', )
    extra = 0


@admin.register(Program)
class ProgramAdmin (admin.ModelAdmin):

    list_display = ('name', 'sys_name', )
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name',)
        }),
        ('Telegram', {
            'fields': ('description', 'file', 'url', )
        }),
    )
    search_fields = ('name', 'sys_name', 'description', 'file', 'url', )
    inlines = [ProgramPeriodInlineTabularAdmin]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):

    def address_short(self, obj):
        s = str(obj.address)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    address_short.short_description = _('Address')

    list_display = ('name', 'contact', 'phone', 'inn', 'city', 'address_short', 'loyalty_department',
                    'loyalty_program', 'loyalty_1c_code')
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'contact', 'phone', 'inn', 'city', 'address', 'agent', 'price_type', )
        }),
        (_('Loyalty'), {
            'fields': ('loyalty_department', 'loyalty_program', 'loyalty_1c_code', 'loyalty_1c_user', )
        }),
        (_('1с values'), {
            'fields': ('loyalty_plan', 'loyalty_fact', 'loyalty_cashback', 'loyalty_sumcashback', 'loyalty_debt',
                       'loyalty_overdue_debt')
        }),
    )
    search_fields = ['name', 'contact', 'phone', 'address', 'inn', 'city', 'loyalty_1c_code',
                     'loyalty_department__name', 'loyalty_program__name', 'agent', 'price_type']
    list_select_related = ('loyalty_department', 'loyalty_program', )
    list_filter = ('loyalty_department', 'loyalty_program',)
