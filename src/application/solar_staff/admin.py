from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportMixin
from import_export.formats.base_formats import CSV, XLSX

from .models import SolarStaffPayments, SolarStaffAccount, Payment
from .resources import PaymentResource


@admin.register(SolarStaffAccount)
class SolarStaffAccountAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        (_('Solar staff data'), {
            'fields': ('salt', 'client_id', )
        }),
    )
    search_fields = ['name', 'salt', 'client_id']


@admin.register(SolarStaffPayments)
class SolarStaffPaymentsAdmin(admin.ModelAdmin):

    def get_user(self, obj):
        if obj.te:
            return obj.te.user
        if obj.order:
            return obj.order.user
        return '-'
    get_user.short_description = _('User')

    def get_task(self, obj):
        if obj.te:
            return obj.te.task
        return '-'
    get_task.short_description = _('Task')

    def get_store(self, obj):
        if obj.te:
            return obj.te.store
        if obj.order:
            return obj.order.store
        return '-'
    get_store.short_description = _('Store')

    def get_status_html(self, obj):
        if obj.server_code == 100:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_server_code_display())
        else:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_server_code_display())
    get_status_html.allow_tags = True
    get_status_html.short_description = _('Status')

    list_display = ('date_payed', 'get_user', 'get_task', 'get_store', 'order', 'type', 'sum', 'get_status_html',
                    'account', )
    list_display_links = ('date_payed', )

    fieldsets = (
        (None, {
            'fields': ('account', 'te', 'order', 'type', 'sum')
        }),
        (_('User data'), {
            'fields': ('email', 'first_name', 'last_name',)
        }),
        (_('Solar staff server answer'), {
            'fields': ('server_code', 'server_error', 'server_response',)
        }),
        (_('Dates'), {
            'fields': ('date_payed',)
        }),
    )

    date_hierarchy = 'date_payed'
    readonly_fields = ('date_payed',)
    list_filter = ('account', 'server_code', 'type')
    search_fields = ['te__task__name', 'te__user__username', 'te__user__first_name', 'te__user__last_name',
                     'te__user__telegram_id', 'te__user__phone', 'te__user__name', 'te__user__surname',
                     'te__store__address', 'server_code', 'server_error', 'server_response', 'email', 'first_name',
                     'last_name', 'te__user__email', 'order__id', 'order__user__username', 'order__user__first_name',
                     'order__user__last_name', 'order__user__telegram_id', 'order__user__phone', 'order__user__name',
                     'order__user__surname', 'order__comment', 'order__delivery_address', 'account__name']
    raw_id_fields = ['te', 'order']
    list_select_related = ('te', 'te__user', 'te__task', 'order', 'order__user', 'te__store', 'te__store__client',
                           'order__store', 'account')


class PaymentAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PaymentAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PaymentAdminForm, self).clean()
        if self.cleaned_data.get('status', None) == 2 and self.request.user.email not in settings.SOLAR_STAFF_USERS:
            raise ValidationError({
                'status': _('You do not have rights to set this status.')
            })
        return cleaned_data


def set_status_pay_solar(modeladmin, request, queryset):
    if request.user.email in settings.SOLAR_STAFF_USERS:
        c = queryset.count()
        for i in queryset:
            i.status = 2
            i.save()
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message='[{"changed": {"fields": ["status"]}}]')
        modeladmin.message_user(request, _('%s items made changed status') % c)
    else:
        modeladmin.message_user(request, _('You do not have rights to set this status.'), level=messages.ERROR)


set_status_pay_solar.short_description = _('Mark selected item status pay in solar')


@admin.register(Payment)
class PaymentAdmin(ImportMixin, admin.ModelAdmin):

    def status_html(self, obj):
        if obj.status == 1:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_status_display())
        if obj.status == 2:
            return mark_safe('<span style="">%s</span>' % obj.get_status_display())
        if obj.status == 3:
            return mark_safe('<b style="color: green">%s</b>' % obj.get_status_display())
        if obj.status == 4:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_status_display())
        return obj.get_status_display()
    status_html.allow_tags = True
    status_html.short_description = _('Status')

    def comment_short(self, obj):
        s = str(obj.comment)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    comment_short.short_description = _('Comment')

    list_display = ('date_create', 'user', 'sum', 'status_html', 'ss_account', 'comment_short')
    list_display_links = ('date_create', 'user', )

    fieldsets = (
        (None, {
            'fields': ('user', 'sum', 'status', 'comment', )
        }),
        (_('Dates'), {
            'fields': ('date_create', 'date_payment', )
        }),
        (_('Solar Staff'), {
            'fields': ('ss_account',)
        }),
    )

    search_fields = ['user__last_name', 'user__first_name', 'user__username', 'comment', 'user__email', 'user__advisor']
    date_hierarchy = 'date_create'
    readonly_fields = ('date_create', 'date_payment')
    raw_id_fields = ('user', )
    list_select_related = ('user', 'ss_account')
    list_filter = ('status', 'ss_account')
    actions = [set_status_pay_solar]
    form = PaymentAdminForm
    resource_class = PaymentResource
    formats = (CSV, XLSX, )
