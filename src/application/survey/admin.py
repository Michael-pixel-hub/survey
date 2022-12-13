import urllib
import datetime

from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry, DELETION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction, models
from django.db.models import Q, Exists, OuterRef
from django.forms.models import BaseInlineFormSet
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, NoReverseMatch
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from import_export.admin import ExportMixin
from import_export.formats.base_formats import DEFAULT_FORMATS, XLSX
from public_model.admin import public_model
from sort_model.admin import order_model_inline, order_model

from application.iceman.models import Store as IcemanStore
from application.survey.models import Assortment as StoreAssortment
from application.survey.models.te import TasksExecutionOutReason

from .filters import CodeFilter, TaskFilter, RegionFilter, ClientFilter
from .forms import TaskStepForm
from .models import User, Client, Store, Good, Task, TasksExecution, Agreement, Assortment, TasksExecutionImage, \
    Import, Region, Category, StoreTask, TasksExecutionAssortment, TasksExecutionCheck, TasksExecutionAssortmentBefore,\
    Rank, UserStatus,  UploadRequests, TaskCustomer, Request, Act, ActCheck, TaskQuestionnaire, \
    TaskQuestionnaireQuestion, TaskStep, TasksExecutionQuestionnaire, Sms, StoreTaskAvail, TasksExecutionInspector, \
    UserDevice, ExternalRequests, UserDeviceIceman, Bank, OutReason, TasksExecutionCheckInspector, UserDelete, \
    UserStatusIceman, TasksExecutionStep, UserSub, Penalty, PenaltyRepayment
from .resources import UserResource, GoodResource, StoreResource


class UserDeviceInlineTabularAdmin(admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False

    model = UserDevice
    fields = ('date_use', 'date_create', 'name', 'os', 'os_version', 'version')
    readonly_fields = ('date_use', 'date_create', )
    extra = 0
    verbose_name = 'Мобильное устройство Сюрвеер'
    verbose_name_plural = 'Мобильные устройства Сюрвеер'


class UserDeviceIcemanInlineTabularAdmin(admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False

    model = UserDeviceIceman
    fields = ('date_use', 'date_create', 'name', 'os', 'version')
    readonly_fields = ('date_use', 'date_create',)
    extra = 0
    verbose_name = 'Мобильное устройство Айсмен'
    verbose_name_plural = 'Мобильные устройства Айсмен'


@order_model_inline
class UserSubInlineTabularAdmin(admin.TabularInline):
    fk_name = 'user'
    model = UserSub
    fields = ('user_sub', )
    extra = 0
    raw_id_fields = ('user_sub',)


@admin.register(User)
class UserAdmin (ExportMixin, admin.ModelAdmin):

    """
    Администрирование пользователей
    """

    user = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('status', 'status_agent', 'status_iceman', 'rank')
        return queryset

    def taxpayer_full(self, obj):
        have_rights = not (self.user is None or self.user.email not in settings.TAXPAYERS_STAFF_USERS)
        html = render_to_string('admin/fields/taxpayer_full.html', {'have_rights': have_rights, 'obj': obj})
        return mark_safe(html)
    taxpayer_full.allow_tags = True
    taxpayer_full.short_description = ''

    def get_form(self, request, obj=None, change=False, **kwarg):
        self.user = request.user
        return super().get_form(request, obj, change, **kwarg)

    list_display = ('fio', 'advisor', 'email', 'route', 'date_join', 'phone', 'is_register',
                    'is_banned', 'rank', 'status_legal', 'source')
    list_display_links = ('fio', )

    fieldsets = (
        (_('Source'), {
            'fields': ('source',)
        }),
        (_('State'), {
            'fields': ('type', 'is_only_self_tasks', 'status', 'status_agent', 'status_legal',
                       'qlik_status', 'route', )
        }),
        ('Айсмен', {
            'fields': ('status_iceman', 'worker_bonus_iceman', )
        }),
        (_('Dates'), {
            'fields': ('date_join', )
        }),
        (_('Rank'), {
            'fields': ('rank', 'is_fixed_rank',)
        }),
        (_('Personal data'), {
            'fields': ('is_register', 'phone', 'name', 'surname', 'advisor', 'email', 'city', )
        }),
        (_('Telegram data'), {
            'fields': ('username', 'first_name', 'last_name', 'language_code', 'telegram_id',)
        }),
        (_('Taxpayer data'), {
            'fields': ('taxpayer_full', )
        }),
        # (_('Taxpayer'), {
        #     'fields': ('taxpayer_status', 'taxpayer_fio', 'taxpayer_passport', 'taxpayer_inn', 'taxpayer_email',
        #                'taxpayer_phone', 'taxpayer_date', 'taxpayer_surname', 'taxpayer_name', 'taxpayer_patronymic',
        #                'taxpayer_passport_series', 'taxpayer_passport_number', 'taxpayer_bank',
        #                'taxpayer_bank_account')
        # }),
        ('Отслеживать координаты', {
            'fields': ('save_geo', 'save_geo_time',)
        }),
        (_('Security'), {
            'fields': ('api_key', 'is_banned', 'is_testing',)
        }),
    )
    readonly_fields = ('date_join', 'taxpayer_full', )
    search_fields = ('username', 'first_name', 'last_name', 'language_code', 'telegram_id', 'phone', 'name', 'surname',
                     'bank_card', 'e_money', 'email', 'source', 'rank__name', 'route')
    date_hierarchy = 'date_join'
    list_filter = ('is_register', 'is_banned', 'type', 'status', 'status_agent', 'status_iceman', 'status_legal',
                   'taxpayer_status', 'source', 'rank', 'is_fixed_rank', 'is_only_self_tasks', )
    list_select_related = ('status', 'status_agent', 'status_iceman', 'rank')
    resource_class = UserResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)
    inlines = (UserSubInlineTabularAdmin, UserDeviceInlineTabularAdmin, UserDeviceIcemanInlineTabularAdmin)


@admin.register(UserDevice)
class UserDeviceAdmin (admin.ModelAdmin):

    list_display = ('user', 'date_create', 'date_use', 'name', 'os', 'version', )
    list_display_links = ('user', 'date_create', )

    fieldsets = (
        (_('Dates'), {
            'fields': ('date_create', 'date_use',)
        }),
        (_('Data'), {
            'fields': ('user', 'name', 'os', 'version', 'key', )
        }),
    )
    readonly_fields = ('date_create', 'date_use',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__telegram_id', 'user__phone',
                     'user__name', 'user__surname', 'user__email', 'name', 'os', 'key', 'version']
    date_hierarchy = 'date_create'
    list_filter = ('os', )
    list_select_related = ('user', )
    raw_id_fields = ('user',)


@admin.register(UserDeviceIceman)
class UserDeviceIcemanAdmin (admin.ModelAdmin):

    list_display = ('user', 'date_create', 'date_use', 'name', 'os', 'version', )
    list_display_links = ('user', 'date_create', )

    fieldsets = (
        (_('Dates'), {
            'fields': ('date_create', 'date_use',)
        }),
        (_('Data'), {
            'fields': ('user', 'name', 'os', 'version', 'key', )
        }),
    )
    readonly_fields = ('date_create', 'date_use',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__telegram_id', 'user__phone',
                     'user__name', 'user__surname', 'user__email', 'name', 'os', 'key', 'version']
    date_hierarchy = 'date_create'
    list_filter = ('os', )
    list_select_related = ('user', )
    raw_id_fields = ('user',)


@admin.register(UserDelete)
class UserDeleteAdmin (admin.ModelAdmin):

    list_display = ('user', 'date_create', 'notification_send', 'notification_date', )
    list_display_links = ('user', 'date_create', )

    fieldsets = (
        (_('Data'), {
            'fields': ('user', 'notification_send')
        }),
        (_('Dates'), {
            'fields': ('date_create', 'notification_date')
        }),
    )
    readonly_fields = ('date_create',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__telegram_id', 'user__phone',
                     'user__name', 'user__surname', 'user__email']
    date_hierarchy = 'date_create'
    list_select_related = ('user', )
    raw_id_fields = ('user',)
    list_filter = ('notification_send',)


@admin.register(Act)
class ActAdmin (admin.ModelAdmin):

    list_display = ('number', 'date', 'user', 'user_fio', 'user_inn', 'user_email', 'sum', 'date_update',
                    'check_type')
    list_display_links = ('number', 'date')

    fieldsets = (
        (None, {
            'fields': ('number', 'id_1c', 'sum')
        }),
        (_('User'), {
            'fields': ('user', 'user_fio', 'user_inn', 'user_phone', 'user_email')
        }),
        (_('Dates'), {
            'fields': ('date', 'date_update', 'date_start', 'date_end')
        }),
        (_('Flags'), {
            'fields': ('is_sent_telegram', )
        }),
        (_('Check'), {
            'fields': ('url', 'check_type', 'check_user', 'comment_manager')
        }),
    )
    readonly_fields = ('date_update', )
    search_fields = ('user_fio', 'user_inn', 'user_phone', 'user_email', 'number')
    date_hierarchy = 'date'
    list_select_related = ('user', 'check_user', )
    raw_id_fields = ('user', 'check_user', )
    list_filter = ('check_type', 'is_sent_telegram', )


@public_model
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@public_model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@public_model
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@public_model
@admin.register(Store)
class StoreAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ('code', 'factory_code', 'category', 'client', 'region_o', 'address',)
    list_display_links = ('code', )

    fieldsets = (
        (None, {
            'fields': ('code', 'factory_code', 'category', 'client', 'region_o', 'address', )
        }),
        # (_('Tasks'), {
        #     'fields': ('days_of_week', )
        # }),
        (_('Geo location'), {
            'fields': ('auto_coord', 'longitude', 'latitude', )
        }),
    )
    search_fields = ['code', 'client__name', 'region_o__name', 'address', 'category__name', 'factory_code']
    list_select_related = ('region_o', 'client', 'category')
    list_filter = ('category', 'region_o',)
    raw_id_fields = ['client', 'region_o']
    
    list_per_page = 50
    resource_class = StoreResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)


@public_model
@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):

    list_display = ('good', 'store', 'task', 'count', )
    list_display_links = ('good', 'store', 'task', )

    fieldsets = (
        (None, {
            'fields': ('good', 'store', 'task', 'count', )
        }),
    )
    search_fields = ['good__name', 'store__code', 'store__address', 'store__region', 'store__client__name', 'task__name']
    raw_id_fields = ['good', 'store']
    list_select_related = ('good', 'store', 'store__client', 'task')
    list_filter = ('task', )


@public_model
@admin.register(Good)
class GoodAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ('name', 'code', )
    list_display_links = ('name', 'code', )

    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description', 'image', )
        }),
    )
    search_fields = ['name', 'description', 'code']

    resource_class = GoodResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)


@public_model
@admin.register(TaskCustomer)
class TaskCustomerAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@order_model_inline
class TaskStepInlineTabularAdmin(admin.StackedInline):
    model = TaskStep
    fields = ('name', 'text', 'step_type', 'photo_from_gallery', 'photo_inspector', 'photo_check_assortment', 
              'photo_check', 'photo_out_reason', 'photo_out_requires', 'questionnaire', 'require', 'is_public')
    extra = 0
    form = TaskStepForm


@public_model
@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):

    class Media:
        js = ()
        css = {
            'all': ('/static/admin/css/tasks.css',)
        }

    change_form_template = 'admin/change_form_tasks.html'

    list_display = ('name', 'money', 'money_source', 'money_fix', 'only_status', 'customer',
                    'fix_status', 'type', 'application')
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'money', 'money_source', )
        }),
        (_('Instruction'), {
            'fields': ('instruction', 'instruction_url',)
        }),
        (_('Task customer'), {
            'fields': ('customer', )
        }),
        (_('Application'), {
            'fields': ('application', 'ai_project',)
        }),
        (_('Add value'), {
            'fields': ('is_add_money', 'add_days', 'add_money')
        }),
        (_('Remove value'), {
            'fields': ('is_remove_money', 'remove_days', 'remove_ppl', 'remove_money')
        }),
        (_('Payment'), {
            'fields': ('ss_account', 'money_fix', )
        }),
        # ('Сюрвеер', {
        #     'fields': ('is_sales', 'is_parse', 'only_status', 'new_task', 'disable_loyalty')
        # }),
        ('Сюрвеер', {
            'fields': ('is_sales', 'only_status')
        }),
        (_('Iceman'), {
            'fields': ('type', )
        }),
        ('Настройки', {
            'fields': ('fix_status',)
        }),
    )
    search_fields = ['name', 'description', 'customer__name']
    raw_id_fields = ['client', 'store']
    # list_filter = ('is_once', 'per_week')
    list_select_related = ('only_status', 'ss_account', 'customer', 'ai_project', )
    list_filter = ('application', 'ai_project', 'is_sales', 'money_fix', 'only_status', 'type',
                   'is_add_money', 'is_remove_money', 'ss_account', 'customer', 'fix_status', )
    inlines = (TaskStepInlineTabularAdmin, )


@order_model_inline
class TaskQuestionnaireQuestionInlineTabularAdmin (admin.TabularInline):

    model = TaskQuestionnaireQuestion
    fields = ('name', 'question', 'question_type', 'choices', 'require', 'is_public')
    extra = 0


@admin.register(TaskQuestionnaire)
class TaskQuestionnaireAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': ('/static/admin/css/questionnaire.css',)
        }

    change_form_template = 'admin/change_form_questionnaire.html'

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']
    inlines = (TaskQuestionnaireQuestionInlineTabularAdmin, )


def set_status_checked(modeladmin, request, queryset):
    c = queryset.count()
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        if obj.task and obj.task.fix_status and request.user.email not in settings.ADMIN_USERS:
            modeladmin.message_user(request, f'Вы не можете поменять статус задачи "{obj}"', level=messages.ERROR)
            return
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message='[{"changed": {"fields": ["status"]}}]')
    queryset.update(status=3)
    modeladmin.message_user(request, _('%s items made changed status') % c)


set_status_checked.short_description = _('Mark selected item status checked')


def set_status_pay_solar(modeladmin, request, queryset):
    if request.user.email in settings.SOLAR_STAFF_USERS:
        c = queryset.count()
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message='[{"changed": {"fields": ["status"]}}]')
        queryset.update(status=6)
        modeladmin.message_user(request, _('%s items made changed status') % c)
    else:
        modeladmin.message_user(request, _('You do not have rights to set this status.'), level=messages.ERROR)


set_status_pay_solar.short_description = _('Mark selected item status pay in solar')


def set_status_payed(modeladmin, request, queryset):
    c = queryset.count()
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message='[{"changed": {"fields": ["status"]}}]')
    queryset.update(status=4)
    modeladmin.message_user(request, _('%s items made changed status') % c)

set_status_payed.short_description = _('Mark selected item status payed')


def set_status_denied(modeladmin, request, queryset):
    c = queryset.count()
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        if obj.task and obj.task.fix_status:
            modeladmin.message_user(request, f'Вы не можете поменять статус задачи "{obj}"', level=messages.ERROR)
            return
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message='[{"changed": {"fields": ["status"]}}]')
    queryset.update(status=5)
    modeladmin.message_user(request, _('%s items made changed status') % c)

set_status_denied.short_description = _('Mark selected item status denied')


def set_status_completed(modeladmin, request, queryset):
    c = queryset.count()
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        if obj.task and obj.task.fix_status:
            modeladmin.message_user(request, f'Вы не можете поменять статус задачи "{obj}"', level=messages.ERROR)
            return
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message='[{"changed": {"fields": ["status"]}}]')
    queryset.update(status=2)
    modeladmin.message_user(request, _('%s items made changed status') % c)


set_status_completed.short_description = _('Mark selected item status completed')


class ProductImageInlineTabularAdmin (admin.TabularInline):

    def status_html(self, obj):
        return mark_safe(obj.status)

    def image_html(self, obj):
        return mark_safe('<img src="%s" />' % obj.image.url)

    model = TasksExecutionImage
    fields = ('image_html', 'type', 'constructor_step_name', 'status_html', )
    extra = 0
    readonly_fields = ('image_html', 'type', 'constructor_step_name', 'status_html', )
    status_html.allow_tags = True
    status_html.short_description = _('Unique status')
    image_html.allow_tags = True
    image_html.short_description = _('Image')

    def has_add_permission(self, request, obj):
        return False


class TasksExecutionAssortmentInlineTabularAdmin (admin.TabularInline):

    model = TasksExecutionAssortment
    fields = ('constructor_step_name', 'good', 'avail', )
    extra = 0
    #raw_id_fields = ['good']


class TasksExecutionOutReasonInlineTabularAdmin (admin.TabularInline):

    model = TasksExecutionOutReason
    fields = ('good', 'out_reason', 'image')
    extra = 0
    max_num = 0
    can_delete = False


class TasksExecutionStepTabularAdmin (admin.TabularInline):

    model = TasksExecutionStep
    fields = ('date_start', 'date_end', 'name', 'step_type', 'is_skip')
    readonly_fields = ['date_start', 'date_end', 'name', 'step_type', 'is_skip']
    extra = 0
    max_num = 0
    can_delete = False


class TasksExecutionInspectorInlineTabularAdmin (admin.TabularInline):

    model = TasksExecutionInspector
    fields = ('constructor_step_name', 'inspector_link_html', 'inspector_report_id', 'inspector_positions_text',
              'inspector_status', 'inspector_is_alert')
    readonly_fields = ['inspector_link_html']
    extra = 0
    max_num = 0
    can_delete = False


class TasksExecutionAssortmentInlineTabularAdminRO (admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def status(self, obj):
        if StoreAssortment.objects.filter(store=obj.task.store, good__code=obj.good.code).count() > 0:
            return mark_safe('<span style="color: green">Есть в матрице</span>')
        else:
            return mark_safe('<span style="color: blue">Новый товар</span>')
    status.allow_tags = True
    status.short_description = _('Status')

    model = TasksExecutionAssortment
    fields = ('good', 'avail', 'status', )
    readonly_fields = ('status', )
    extra = 0
    can_delete = False
    max_num = 0


class TasksExecutionAssortmentBeforeInlineTabularAdmin (admin.TabularInline):

    model = TasksExecutionAssortmentBefore
    fields = ('good', 'avail', )
    extra = 0
    raw_id_fields = ['good']


class TasksExecutionAssortmentBeforeInlineTabularAdminRO (admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    model = TasksExecutionAssortmentBefore
    fields = ('good', 'avail', )
    extra = 0
    can_delete = False
    max_num = 0
    raw_id_fields = ['good']


class TasksExecutionQuestionnaireInlineTabularAdmin(admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    model = TasksExecutionQuestionnaire

    fields = ('constructor_step_name', 'name', 'question', 'answer', )
    extra = 0
    can_delete = False
    max_num = 0


class TasksExecutionAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TasksExecutionAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TasksExecutionAdminForm, self).clean()
        if self.cleaned_data.get('status', None) == 6 and self.request.user.email not in settings.SOLAR_STAFF_USERS:
            raise ValidationError({
                'status': _('You do not have rights to set this status.')
            })
        return cleaned_data


@admin.register(TasksExecution)
class TasksExecutionAdmin(admin.ModelAdmin):

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '/static/admin/js/move_images.js',
        )

    def save_model(self, request, obj, form, change):

        if obj.status in [3, 5, 8] and obj.audit_user is None:
            obj.audit_user = request.user

        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if request.user.email in settings.ADD_TASK_USERS:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.email in settings.ADD_TASK_USERS:
            return True
        return False

    def changelist_view(self, request, extra_context=None):

        user_id = None
        user_name = ''
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            try:
                user_obj = User.objects.get(id=user_id)
                label = ''
                if user_obj.fio.strip() != '':
                    label += f'{user_obj.fio} '
                if user_obj.phone:
                    label += f'{user_obj.phone} '
                if user_obj.email:
                    label += f'{user_obj.email} '
                if not label:
                    label = f'Пользователь # {user_obj.id}'
                user_name = label
            except:
                user_id = None

        store_id = None
        store_name = ''
        if request.GET.get('store_id'):
            store_id = request.GET.get('store_id')
            try:
                store_obj = Store.objects.get(id=store_id)
                store_name = str(store_obj)
            except:
                store_id = None

        task_id = None
        task_name = ''
        if request.GET.get('task_id'):
            task_id = request.GET.get('task_id')
            try:
                task_obj = Task.objects.get(id=task_id)
                task_name = task_obj.name
            except:
                task_id = None

        cl = self.get_changelist_instance(request)
        extra_context = {
            'PARAM_USER_URL': cl.get_query_string({'user_id': 'USER_ID'}),
            'PARAM_USER_URL_CLEAR': cl.get_query_string(remove=['user_id']),
            'PARAM_USER_ID': user_id,
            'PARAM_USER_NAME': user_name,
            'PARAM_STORE_URL': cl.get_query_string({'store_id': 'STORE_ID'}),
            'PARAM_STORE_URL_CLEAR': cl.get_query_string(remove=['store_id']),
            'PARAM_STORE_ID': store_id,
            'PARAM_STORE_NAME': store_name,
            'PARAM_TASK_ID': task_id,
            'PARAM_TASK_NAME': task_name,
            'PARAM_TASK_URL': cl.get_query_string({'task_id': 'TASK_ID'}),
            'PARAM_TASK_URL_CLEAR': cl.get_query_string(remove=['task_id']),
        }
        return super().changelist_view(request, extra_context)

    def get_list_display(self, request):
        ls = request.user.task.values_list('id', flat=True)
        if ls:
            return ('user_object', 'user_name', 'user_surname', 'task_object', 'date_start', 'date_end', 'store_short',
                    'check', 'is_auditor', 'application', 'source', 'get_status_html', 'is_fake_gps', 'is_api_direct', )
        return self.list_display

    def get_inline_instances(self, request, obj=None):
        if obj is not None and obj.task is not None and obj.task.new_task:
            _inlines = [ProductImageInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionStepTabularAdmin(self.model, self.admin_site),
                        TasksExecutionQuestionnaireInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionAssortmentInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionInspectorInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionOutReasonInlineTabularAdmin(self.model, self.admin_site),
                        ]
        else:
            _inlines = [ProductImageInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionStepTabularAdmin(self.model, self.admin_site),
                        TasksExecutionAssortmentBeforeInlineTabularAdmin(self.model, self.admin_site),
                        TasksExecutionAssortmentInlineTabularAdmin(self.model, self.admin_site)]
        filters = request.GET.get('_changelist_filters')
        is_simple = False
        if filters and 'date_start__gte' in filters and 'date_start__lte' in filters and 'user__id' in filters:
            is_simple = True
        if is_simple:
            return [TasksExecutionAssortmentBeforeInlineTabularAdminRO(self.model, self.admin_site),
                    TasksExecutionAssortmentInlineTabularAdminRO(self.model, self.admin_site),
                    ]
        return _inlines

    def get_form(self, request, obj=None, **kwargs):

        AdminForm = super(TasksExecutionAdmin, self).get_form(request, obj, **kwargs)

        class TasksExecutionRequestAdminForm(AdminForm):

            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return TasksExecutionRequestAdminForm

    def get_status_html(self, obj):
        if obj.status == 1:
            return mark_safe('<span style="color: gray">%s</span>' % obj.get_status_display())
        if obj.status == 3:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_status_display())
        if obj.status == 4:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_status_display())
        if obj.status == 5:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_status_display())
        if obj.status == 6:
            return mark_safe('<b>%s</b>' % obj.get_status_display())
        return obj.get_status_display()
    get_status_html.allow_tags = True
    get_status_html.short_description = _('Status')

    # def store_short(self, obj):
    #     s = str(obj.store)
    #     if len(s) > 100:
    #         s = s[:100] + '...'
    #     return s
    # store_short.short_description = _('Store')

    def get_readonly_fields(self, request, obj=None):
        ls = request.user.task.values_list('id', flat=True)
        filters = request.GET.get('_changelist_filters')
        is_simple = False
        if filters and 'date_start__gte' in filters and 'date_start__lte' in filters and 'user__id' in filters:
            is_simple = True

        r_list = self.readonly_fields.copy()

        if is_simple:
            r_list = 'date_start', 'map_html', 'user_object', 'user_name', 'user_surname', 'task', 'date_start', \
                   'date_end', 'store_iceman', 'user', \
                   'store', 'status', 'check', 'is_auditor', 'comments', 'longitude', 'latitude', 'distance', \
                   'comments_status', 'inspector_link_html', 'money', 'money_source', 'step', 'check_type', \
                   'check_user', 'audit_user', 'date_end_user', 'inspector_is_work', 'inspector_link_html', \
                    'inspector_status', 'inspector_status_before', 'inspector_error', 'inspector_upload_images_text', \
                   'inspector_recognize_text', 'inspector_report_text', 'inspector_positions_text', \
                   'inspector_report_id', 'inspector_report_id_before', 'inspector_is_alert', \
                   'telegram_channel_status', 'comments_internal', 'images_simple_before', 'images_simple_after',\
                   'images_simple_check', 'store_assortment_full', 'constructor_step', 'source', 'task_object', \
                   'application'
        elif ls:
            r_list = 'date_start', 'map_html', 'user_object', 'user_name', 'user_surname', 'task', 'date_start', \
                     'date_end', 'store', 'store_iceman', 'status', 'check',  'is_auditor', 'comments', 'longitude', \
                     'latitude', 'distance', 'comments_status', 'inspector_link_html', 'store_assortment_full', \
                     'step', 'date_end_user', 'constructor_step', 'source', 'task_object', 'application', 'status', \
                     'is_auditor', 'comments_status', 'check_type', 'audit_user', 'check_user'

        if obj and obj.task and obj.task.fix_status and request.user.email not in settings.ADMIN_USERS:
            r_list += ('status', )

        return r_list

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'constructor_step':
            obj_id = request.resolver_match.kwargs['object_id']
            obj = TasksExecution.objects.get(id=obj_id)
            kwargs['queryset'] = TaskStep.objects.filter(task=obj.task)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        ls = request.user.task.values_list('id', flat=True)
        filters = request.GET.get('_changelist_filters')
        is_simple = False
        if filters and 'date_start__gte' in filters and 'date_start__lte' in filters and 'user__id' in filters:
            is_simple = True
        step = 'constructor_step' if obj is not None and obj.task is not None and obj.task.new_task else 'step'
        if is_simple:
            return (
                (None, {
                    'fields': ('store', 'store_iceman', 'comments', 'date_end_user', 'application', 'source', )
                }),
                (_('Images'), {
                    'fields': ('images_simple_before', 'images_simple_after', 'images_simple_check')
                }),
                (_('Task execution'), {
                    'classes': ('collapse',),
                    'fields': ('user', 'task', 'money', 'money_source', 'store', step, )
                }),
                (_('Comments'), {
                    'classes': ('collapse',),
                    'fields': ('comments_internal',)
                }),
                (_('Status'), {
                    'classes': ('collapse',),
                    'fields': ('status', 'comments_status', 'check', 'check_type', 'is_auditor', 'audit_user',
                       'check_user')
                }),
                (_('Dates'), {
                    'classes': ('collapse',),
                    'fields': ('date_start', 'date_end_user', 'date_end',)
                }),
                (_('Coordinates'), {
                    'classes': ('collapse',),
                    'fields': ('longitude', 'latitude', 'map_html', 'distance',)
                }),
                (_('Inspector'), {
                    'classes': ('collapse',),
                    'fields': (
                    'inspector_is_work', 'inspector_link_html', 'inspector_status', 'inspector_status_before',
                    'inspector_error',
                    'inspector_upload_images_text', 'inspector_recognize_text', 'inspector_report_text',
                    'inspector_positions_text', 'inspector_report_id', 'inspector_report_id_before',
                    'inspector_is_alert',)
                }),
                (_('Mailing'), {
                    'classes': ('collapse',),
                    'fields': ('telegram_channel_status',)
                }),
                (_('AVAIL ASSORTMENT STORE'), {
                    'fields': ('store_assortment_full',)
                }),
            )
        if ls:
            return (
                (None, {
                    'fields': ('user', 'task', 'store', 'store_iceman', step, 'application', 'source',)
                }),
                (_('Comments'), {
                    'fields': ('comments',)
                }),
                (_('Status change'), {
                    'fields': ('status', 'comments_status', 'check', 'check_type', 'is_auditor', 'audit_user',
                       'check_user')
                }),
                (_('Dates'), {
                    'fields': ('date_start', 'date_end_user', 'date_end',)
                }),
                (_('Coordinates'), {
                    'fields': ('longitude', 'latitude', 'map_html', 'distance',)
                }),
                (_('AVAIL ASSORTMENT STORE'), {
                    'fields': ('store_assortment_full',)
                }),
            )
        return (
            (None, {
                'fields': ('user', 'task', 'money', 'money_source', 'store', 'store_iceman', step, 'application')
            }),
            (_('Comments'), {
                'fields': ('comments', 'comments_internal',)
            }),
            (_('Status change'), {
                'fields': ('status', 'comments_status', 'check', 'check_type', 'is_auditor', 'audit_user',
                       'check_user')
            }),
            (_('Dates'), {
                'fields': ('date_start', 'date_end_user', 'date_end',)
            }),
            ('Источник', {
                'fields': ('source', 'source_name', 'source_os', 'source_os_version', 'source_version', 'is_fake_gps',
                           'is_api_direct')
            }),
            (_('Coordinates'), {
                'fields': ('longitude', 'latitude', 'map_html', 'distance',)
            }),
            (_('Inspector'), {
                'classes': ('collapse',),
                'fields': ('inspector_is_work', 'inspector_link_html', 'inspector_status', 'inspector_status_before',
                           'inspector_error', 'inspector_upload_images_text', 'inspector_recognize_text',
                           'inspector_report_text', 'inspector_positions_text', 'inspector_report_id',
                           'inspector_report_id_before', 'inspector_is_alert',)
            }),
            (_('Mailing'), {
                'classes': ('collapse',),
                'fields': ('telegram_channel_status',)
            }),
            (_('AVAIL ASSORTMENT STORE'), {
                'fields': ('store_assortment_full',)
            }),
        )

    def map_html(self, obj):

        s = '''
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
   integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
   crossorigin=""/>
        <!-- Make sure you put this AFTER Leaflet's CSS -->
 <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
   integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
   crossorigin=""></script>
        <style>
            .field-status_html p  {font-size: 16px !important}
            #task_images-group {max-height: 800px; overflow-y: scroll}
            #map {width:800px; height:400px}
        </style>
        <div id="map"></div>
        <script type="text/javascript">
            $().ready(function () {
                var map = L.map('map', {minZoom: 1, maxZoom: 18}).setView([{latitude}, {longitude}], 16);
                  
//L.tileLayer('https://{s}.tilessputnik.ru/{z}/{x}/{y}.png', {
    //attribution: ''
//}).addTo(map);   
                
L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: ''
}).addTo(map);          

var LeafIcon = L.Icon.extend({
    options: {
       iconSize:     [34, 41],
       iconAnchor:   [12, 37],
       popupAnchor:  [2, -36]
    }
});

var greenIcon = new LeafIcon({
    iconUrl: '/static/map_osm/images/green.png'
})     
var redIcon = new LeafIcon({
    iconUrl: '/static/map_osm/images/red.png'
})                                     
                    
                var marker = L.marker([{latitude}, {longitude}], {icon: greenIcon}).addTo(map);                
                var marker_store = L.marker([{store_latitude}, {store_longitude}], {icon: redIcon}).addTo(map);                
                var bounds = [[{latitude}, {longitude}], [{store_latitude}, {store_longitude}]];
                var pathLine = L.polyline([[{latitude}, {longitude}], [{store_latitude}, {store_longitude}]], {color: "#3985db", weight: 4}).addTo(map);
                
                if ({distance} < 0.14) {
                    var popup = L.popup().setContent('{distance} км');                                
                    pathLine.bindPopup(popup);
                    var popup2 = L.popup().setContent('Местонахождение сюрвеера');                                
                    marker.bindPopup(popup2);
                    var popup3 = L.popup().setContent('Местонахождение магазина');                                
                    marker_store.bindPopup(popup3) ;                      
                } else {
                    var popup = L.popup({closeOnClick: false, autoClose: false}).setContent('{distance} км');                                
                    pathLine.bindPopup(popup).openPopup();
                    var popup2 = L.popup({closeOnClick: false, autoClose: false}).setContent('Местонахождение сюрвеера');                                
                    marker.bindPopup(popup2).openPopup();       
                    var popup3 = L.popup({closeOnClick: false, autoClose: false}).setContent('Местонахождение магазина');                                
                    marker_store.bindPopup(popup3).openPopup();                        
                }                                                      
                map.fitBounds(bounds, {paddingTopLeft: [50, 50]});   
                //alert(map.getBoundsZoom());   
            });
        </script>
        '''

        s = s.replace('{longitude}', str(obj.longitude))
        s = s.replace('{latitude}', str(obj.latitude))
        s = s.replace('{store_longitude}', str(obj.store.longitude))
        s = s.replace('{store_latitude}', str(obj.store.latitude))
        try:
            s = s.replace('{distance}', str(obj.distance / 1000))
        except:
            s = s.replace('{distance}', '0')

        if obj.distance:
            return mark_safe(s)
        else:
            return mark_safe('-')

        # s = '''
        #     <style type="text/css">
        #         .field-status_html p  {font-size: 16px !important}
        #         #task_images-group { max-height: 800px; overflow-y: scroll}
        #     </style>
        #     <script src="https://api-maps.yandex.ru/1.1/index.xml" type="text/javascript"></script>
        #     <div id="YMapsID" style="width:800px;height:400px"></div>
        #     <script type="text/javascript">
        #         $().ready(function () {
        #             $('#tasksexecution_form div .module:nth-child(8)').insertAfter('#task_images-group');
        #             $('#tasksexecution_form div .module:nth-child(3)').insertAfter('#task_images-group');
        #         });
        #         YMaps.jQuery(function () {
        #
        #             var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);
        #             map.setCenter(new YMaps.GeoPoint({longitude}, {latitude}), 16);
        #             map.addControl(new YMaps.TypeControl());
        #             map.addControl(new YMaps.ToolBar());
        #             map.addControl(new YMaps.Zoom());
        #             map.addControl(new YMaps.ScaleLine());
        #
        #             var placemark = new YMaps.Placemark(new YMaps.GeoPoint({store_longitude}, {store_latitude}), {style: "default#shopIcon", hasHint: true})
        #             placemark.setIconContent("Щелкни меня");
        #             placemark.name = "Магазин";
        #             map.addOverlay(placemark);
        #
        #             var placemark = new YMaps.Placemark(new YMaps.GeoPoint({longitude}, {latitude}), {style: "default#photographerIcon", hasHint: true})
        #             placemark.setIconContent("Пользователь");
        #             placemark.name = "Пользователь";
        #             map.addOverlay(placemark);
        #
        #             var bounds = new YMaps.GeoBounds(new YMaps.GeoPoint({store_longitude}, {store_latitude}), new YMaps.GeoPoint({longitude}, {latitude}));
        #             //map.setBounds(bounds, {checkZoomRange:true});
        #             //map.setZoom(map.getZoom() - 1)
        #
        #             var s = new YMaps.Style();
        #             s.lineStyle = new YMaps.LineStyle();
        #             s.lineStyle.strokeColor = '6B8E23';
        #             s.lineStyle.strokeWidth = '5';
        #             YMaps.Styles.add("example#CustomLine", s);
        #
        #             var pl = new YMaps.Polyline([
        #                 new YMaps.GeoPoint({store_longitude}, {store_latitude}),
        #                 new YMaps.GeoPoint({longitude}, {latitude})
        #             ], {hasHint: 1, hasBalloon: 1});
        #
        #             pl.name = "{distance} км";
        #             pl.setStyle("example#CustomLine");
        #
        #             map.addOverlay(pl);
        #         })
        #     </script>
        # '''
        # s = s.replace('{longitude}', str(obj.longitude))
        # s = s.replace('{latitude}', str(obj.latitude))
        # s = s.replace('{store_longitude}', str(obj.store.longitude))
        # s = s.replace('{store_latitude}', str(obj.store.latitude))
        # s = s.replace('{distance}', str(obj.distance))
        # if obj.distance:
        #     return mark_safe(s)
        # else:
        #     return mark_safe('-')
    map_html.allow_tags = True
    map_html.short_description = _('Map')

    def images_simple_before(self, obj):
        if obj.task is not None and obj.task.new_task:
            images = TasksExecutionImage.objects.filter(task=obj, constructor_step_name__icontains='до')
        else:
            images = TasksExecutionImage.objects.filter(task=obj, type='before')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_before.allow_tags = True
    images_simple_before.short_description = _('Images before')

    def images_simple_after(self, obj):
        if obj.task is not None and obj.task.new_task:
            images = TasksExecutionImage.objects.filter(task=obj, constructor_step_name__icontains='после')
        else:
            images = TasksExecutionImage.objects.filter(task=obj, type='after')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_after.allow_tags = True
    images_simple_after.short_description = _('Images after')

    def images_simple_check(self, obj):
        if obj.task is not None and obj.task.new_task:
            images = TasksExecutionImage.objects.filter(task=obj, constructor_step_name__icontains='чек')
        else:
            images = TasksExecutionImage.objects.filter(task=obj, type='check')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_check.allow_tags = True
    images_simple_check.short_description = _('Images check')

    def store_assortment_full(self, obj):
        goods = list(StoreAssortment.objects.filter(store=obj.store, task=obj.task))
        if not goods:
            goods = list(StoreAssortment.objects.filter(store=obj.store, task__isnull=True))
        goods_after = TasksExecutionAssortment.objects.filter(task=obj)
        data = []
        for i in goods:
            item = {'name': i.good.name, 'in_store': False, 'count': i.count}
            for j in goods_after:
                if (i.good.code and i.good.code == j.good.code) or (i.good.name and i.good.name == j.good.name):
                    item['in_store'] = True
            data.append(item)
        html = render_to_string('admin/fields/store_assortment_full.html', {'data': data})
        return mark_safe(html)
    store_assortment_full.allow_tags = True
    store_assortment_full.short_description = ''

    def get_search_results(self, request, queryset, search_term):
        if not search_term or len(search_term) < 3:
            return super().get_search_results(
                request, queryset, search_term
            )
        stores = Store.objects.filter(
            Q(address__search=search_term) | Q(code__contains=search_term)
        ).values_list('id', flat=True)
        iceman_stores = IcemanStore.objects.filter(
            Q(address__search=search_term) | Q(code__contains=search_term) | Q(name__search=search_term)
        ).values_list('id', flat=True)
        queryset = queryset.filter(Q(store_id__in=list(stores)) | Q(store_iceman_id__in=list(iceman_stores)))
        return queryset, False

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('user', 'store', 'task', 'store__client', 'user__rank')
        if not request.user.is_superuser and request.user.task:
            queryset = queryset.filter(task__in=request.user.task.values_list('id', flat=True))
        return queryset

    form = TasksExecutionAdminForm

    list_display = ('user_object', 'user_name', 'user_surname', 'task_object', 'date_start', 'date_end', 'store_short',
                    'money', 'check', 'is_auditor', 'application', 'source', 'get_status_html', 'is_fake_gps',
                    'is_api_direct', )
    list_display_links = ('user_object', )

    fieldsets = (
        (None, {
            'fields': ('user', 'task', 'money', 'money_source', 'store', 'store_iceman', 'step', )
        }),
        (_('Comments'), {
            'fields': ('comments', 'comments_internal',)
        }),
        (_('Status change'), {
            'fields': ('status', 'comments_status', 'check', 'check_type', 'is_auditor', 'audit_user',
                       'check_user')
        }),
        (_('Dates'), {
            'fields': ('date_start', 'date_end_user', 'date_end', )
        }),
        ('Источник', {
            'fields': ('source', 'source_name', 'source_os', 'source_os_version', 'source_version', 'is_fake_gps',
                       'is_api_direct')
        }),
        (_('Coordinates'), {
            'fields': ('longitude', 'latitude', 'map_html', 'distance',)
        }),
        (_('Inspector'), {
            'classes': ('collapse',),
            'fields': ('inspector_is_work', 'inspector_link_html', 'inspector_status', 'inspector_status_before',
                       'inspector_error',
                       'inspector_upload_images_text', 'inspector_recognize_text', 'inspector_report_text',
                       'inspector_positions_text', 'inspector_report_id', 'inspector_report_id_before',
                       'inspector_is_alert',)
        }),
        (_('Mailing'), {
            'classes': ('collapse',),
            'fields': ('telegram_channel_status',)
        }),
    )
    # search_fields = ['task__name', 'user__username', 'user__first_name', 'user__last_name', 'user__telegram_id',
    #                  'user__phone', 'user__name', 'user__surname', 'user__email', 'store__address', 'comments',
    #                  'inspector_status']
    search_fields = ['store__address', 'store__code']
    raw_id_fields = ['user', 'task', 'store', 'store_iceman']
    readonly_fields = ['date_start', 'map_html', 'inspector_link_html', 'store_assortment_full', 'application',
                       'is_auditor', 'check_type', 'audit_user', 'check_user', 'source_name', 'source_os',
                       'source_os_version', 'source_version', 'is_fake_gps', 'is_api_direct', 'source']
    date_hierarchy = 'date_start'
    list_filter = ('application', 'status', 'source', 'user__status_legal', 'check', 'is_auditor', 'check_type',
                   ClientFilter, RegionFilter, CodeFilter, 'is_fake_gps', 'is_api_direct')
    inlines = [ProductImageInlineTabularAdmin, TasksExecutionStepTabularAdmin,
               TasksExecutionAssortmentBeforeInlineTabularAdmin,
               TasksExecutionAssortmentInlineTabularAdmin, TasksExecutionInspectorInlineTabularAdmin,
               TasksExecutionOutReasonInlineTabularAdmin]
    #list_select_related = ('user', 'store', 'task', 'store__client', 'user__rank')
    list_per_page = 50
    actions = [set_status_checked, set_status_pay_solar, set_status_payed, set_status_denied, set_status_completed]
    #prefetch_related = ('user', 'store', 'task', 'store__client', 'user__rank')


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        add_permission = super().has_add_permission(request)
        if settings.DEBUG:
            return add_permission
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        delete_permission = super().has_delete_permission(request)
        if settings.DEBUG:
            return delete_permission
        else:
            return False

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'file', )
        }),
    )
    search_fields = ['name']

    if not settings.DEBUG:
        actions = None
        readonly_fields = ('name', )


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):

    list_display = ('file_name', 'date_start', 'user', 'date_end', 'rows_count', 'rows_process', 'status')
    list_display_links = ('file_name', 'date_start', )

    fieldsets = (
        (_('File'), {
            'fields': ('file_name', 'file',)
        }),
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Data'), {
            'fields': ('rows_count', 'rows_process', 'status', 'report_text', )
        }),
        (_('Dates'), {
            'fields': ('date_start', 'date_end', )
        }),
    )
    search_fields = ['file_name']
    date_hierarchy = 'date_start'
    readonly_fields = ('date_start',)
    list_filter = ('status',)
    raw_id_fields = ('user',)
    list_select_related = ('user', )


@admin.register(StoreTask)
class StoreTaskAdmin(admin.ModelAdmin):

    def get_store_html(self, obj):
        return mark_safe('<a href="%s">%s</a>' %
                         (reverse('admin:survey_storetask_change', args=[obj.id]), obj.store, ))
    get_store_html.allow_tags = True
    get_store_html.short_description = _('Store')

    list_display = ('task', 'get_store_html', 'is_once', 'per_week', 'days_of_week', 'per_month', 'hours_start',
                    'hours_end', 'position', )
    # 'is_add_value', 'add_value'
    list_display_links = ('task', )

    fieldsets = (
        (None, {
            'fields': ('task', 'store', )
        }),
        (_('Periodicity'), {
            'fields': ('is_once', 'per_week', 'days_of_week', 'per_month', 'hours_start', 'hours_end',)
        }),
        ('Последовательность', {
            'fields': ('position',)
        }),
        (_('Users'), {
            'fields': ('only_user',)
        }),
        (_('Mailing'), {
            'fields': ('telegram_channel_id',)
        }),
        (_('Add value'), {
            'fields': ('is_add_value', 'add_value')
        }),
    )
    search_fields = ['task__name', 'store__address', 'store__address', 'store__code', 'only_user__telegram_id',
                     'only_user__username', 'only_user__email', 'telegram_channel_id']
    raw_id_fields = ['task', 'store', 'only_user']
    list_filter = ('task', 'is_add_value', ClientFilter, RegionFilter)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = [field.name for field in LogEntry._meta.get_fields()]
    list_filter = ['user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    list_display = ['__str__', 'content_type', 'action_time', 'user', 'object_link']
    list_select_related = ('content_type', 'user')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # only for superusers, cannot return False, the module
        # wouldn't be visible in admin
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe('<a href="%s">%s</a>' % (
                                 reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                                         args=[obj.object_id]),
                                 escape(obj.object_repr),
                ))
            except NoReverseMatch:
                link = obj.object_repr
        return link
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


class CheckImageFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(CheckImageFormset, self).__init__(*args, **kwargs)
        self.queryset = TasksExecutionImage.objects.filter(type='check', task=kwargs['instance'])


class CheckImageAdmin (admin.TabularInline):

    def status_html(self, obj):
        return mark_safe(obj.status)

    def image_html(self, obj):
        return mark_safe('<img src="%s" />' % obj.image.url)

    model = TasksExecutionImage
    fields = ('image_html', 'type', 'constructor_step_name', 'status_html', )
    extra = 0
    readonly_fields = ('image_html', 'type', 'constructor_step_name', 'status_html', )
    status_html.allow_tags = True
    status_html.short_description = _('Unique status')
    image_html.allow_tags = True
    image_html.short_description = _('Image')
    formset = CheckImageFormset

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class TasksExecutionCheckForm(forms.ModelForm):

    current_user = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TasksExecutionCheckForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(TasksExecutionCheckForm, self).save(*args, **kwargs)
        if obj.set_check_verified or obj.set_check_not_verified:
            obj.check_user = self.current_user
        obj.save()
        return obj


@admin.register(TasksExecutionCheck)
class TasksExecutionCheckAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': ('admin/css/check_admin.css',)
        }

    def get_queryset(self, request):
        qs = super(TasksExecutionCheckAdmin, self).get_queryset(request)
        qs = qs.filter(check_type='not_verified', status=2, source='telegram')
        # images = TasksExecutionImage.objects.filter(task__id=OuterRef('pk'), type='check')
        # qs = qs.annotate(images_exist=Exists(images)).filter(images_exist=True)
        return qs

    def get_image_html(self, obj):
        image = TasksExecutionImage.objects.filter(type='check', task=obj).first()
        try:
            return mark_safe(
                '<a href="%s" target=blank><img src="%s" style="max-width: 500px; max-height: 500px;" /></a>' %
                (image.image.url, image.image.url)
            )
        except:
            return mark_safe('-')
    get_image_html.allow_tags = True
    get_image_html.short_description = _('Image')

    def get_store_html(self, obj):
        return mark_safe('<a href="%s" target=blank>%s</a>' %
                         (reverse('admin:survey_tasksexecution_change', args=[obj.id]), obj.store, ))
    get_store_html.allow_tags = True
    get_store_html.short_description = _('Store')

    list_display = ('user', 'date_start', 'get_store_html', 'set_check_verified', 'set_check_not_verified', 'get_image_html')
    list_display_links = ('user', )

    fieldsets = (
        (None, {
            'fields': ('user', 'store', 'check_type', 'date_start', )
        }),
    )
    search_fields = ['task__name', 'user__username', 'user__first_name', 'user__last_name', 'user__telegram_id',
                     'user__phone', 'user__name', 'user__surname', 'user__email', 'store__address', 'comments']
    raw_id_fields = ['user', 'store']
    readonly_fields = ['date_start']
    date_hierarchy = 'date_start'
    list_select_related = ('user', 'store', 'task', 'store__client')
    list_filter = (TaskFilter, ClientFilter, RegionFilter, CodeFilter)
    list_per_page = 50
    inlines = [CheckImageAdmin]
    list_editable = ('set_check_verified', 'set_check_not_verified')

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', TasksExecutionCheckForm)
        form = super(TasksExecutionCheckAdmin, self).get_changelist_form(request, **kwargs)
        form.current_user = request.user
        return form


@public_model
@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):

    list_display = ('name', 'default', 'work_days', 'tasks_month', 'tasks_count',  'rate')
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name',  'default', 'work_days', 'tasks_month', 'tasks_count', 'rate', )
        }),
    )
    search_fields = ['name']
    list_filter = ('default', )


@public_model
@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@public_model
@admin.register(UserStatusIceman)
class UserStatusIcemanAdmin(admin.ModelAdmin):

    list_display = ('name', 'default', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'default', )
        }),
    )
    search_fields = ['name']
    list_filter = ('default',)


@admin.register(UploadRequests)
class UploadRequestsAdmin(admin.ModelAdmin):

    def result_short(self, obj):
        s = str(obj.result)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    result_short.short_description = _('Result')

    list_display = ('request_date', 'request_ip', 'request_method', 'request_type', 'request_data_type',
                    'result_short', 'request_data_count', 'processed',)
    list_display_links = ('request_date', 'request_ip', 'request_method', )

    fieldsets = (
        (None, {
            'fields': ('request_date', 'request_ip', 'request_method', 'request_type', 'request_text', 'request_files',
                       'processed', 'request_data_type', 'request_data_count', 'result', )
        }),
    )
    search_fields = ['request_ip', 'request_method', 'request_type', 'request_text', 'request_files', 'result',
                     'request_data_type']
    readonly_fields = ['request_date']
    date_hierarchy = 'request_date'
    list_filter = ('processed', 'request_data_type',)


@admin.register(ExternalRequests)
class ExternalRequestsAdmin(admin.ModelAdmin):

    def result_short(self, obj):
        s = str(obj.result)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    result_short.short_description = _('Result')

    list_display = ('request_date', 'request_ip', 'request_method', 'request_type', 'request_data_type',
                    'result_short', 'request_data_count', 'processed',)
    list_display_links = ('request_date', 'request_ip', 'request_method', )

    fieldsets = (
        (None, {
            'fields': ('request_date', 'request_ip', 'request_method', 'request_type', 'request_text', 'request_files',
                       'processed', 'request_data_type', 'request_data_count', 'result', )
        }),
    )
    search_fields = ['request_ip', 'request_method', 'request_type', 'request_text', 'request_files', 'result',
                     'request_data_type']
    readonly_fields = ['request_date']
    date_hierarchy = 'request_date'
    list_filter = ('processed', 'request_data_type',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = ('date', 'method', 'url', )
    list_display_links = ('date', 'method', )

    fieldsets = (
        (None, {
            'fields': ('date', 'method', 'url', 'body', 'result', )
        }),
    )
    search_fields = ['method', 'body', 'result', 'url']
    readonly_fields = ['date']
    date_hierarchy = 'date'


class ActCheckForm(forms.ModelForm):

    current_user = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super().save(*args, **kwargs)
        if obj.set_check_verified or obj.set_check_not_verified:
            obj.check_user = self.current_user
        obj.save()
        return obj


@admin.register(ActCheck)
class ActCheckAdmin (admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(check_type='wait', url__isnull=False)

    def get_data_html(self, obj):
        date = obj.date.strftime('%d.%m.%Y') if obj.date else '-'
        date_start = obj.date_start.strftime('%d.%m.%Y') if obj.date_start else '-'
        date_end = obj.date_end.strftime('%d.%m.%Y') if obj.date_end else '-'
        return mark_safe(f'<p>{obj.user_fio}</p><p><b>{obj.sum} руб.</b></p><p>{obj.user_inn}</p><p>{date}</p>'
                         f'<p>с {date_start} по {date_end}</p>')
    get_data_html.allow_tags = True
    get_data_html.short_description = _('Data')

    def get_image_html(self, obj):
        return mark_safe(
            f'<a href="{obj.url}" target=blank>'
            f'<img src="{obj.url}" style="max-width: 500px; max-height: 500px; border: 1px solid #eee" />'
            f'</a>'
        )
    get_image_html.allow_tags = True
    get_image_html.short_description = _('Image')

    list_display = ('number', 'comment_manager', 'get_data_html', 'set_check_verified', 'set_check_not_verified',
                    'get_image_html')
    list_display_links = ('number', )
    fieldsets = (
        (None, {
            'fields': ('number', 'sum', 'comment_manager')
        }),
        (_('User'), {
            'fields': ('user', 'user_fio', 'user_inn', 'user_phone', 'user_email')
        }),
        (_('Dates'), {
            'fields': ('date', 'date_start', 'date_end')
        }),
    )
    search_fields = ('user_fio', 'user_inn', 'user_phone', 'user_email', 'number')
    date_hierarchy = 'date'
    list_select_related = ('user', 'check_user', )
    raw_id_fields = ('user', 'check_user', )
    list_editable = ('comment_manager', 'set_check_verified', 'set_check_not_verified')

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', ActCheckForm)
        form = super().get_changelist_form(request, **kwargs)
        form.current_user = request.user
        return form


@admin.register(TasksExecutionInspector)
class TasksExecutionInspectorAdmin(admin.ModelAdmin):

    list_display = ('task', 'constructor_step_name', 'date_start', 'inspector_status', 'inspector_is_alert', )
    list_display_links = ('task', 'constructor_step_name', )

    fieldsets = (
        (None, {
            'fields': ('task', 'constructor_step_name', )
        }),
        (_('Dates'), {
            'fields': ('date_start',)
        }),
        (_('Inspector status'), {
            'fields': ('inspector_status', 'inspector_is_alert')
        }),
        (_('Inspector working'), {
            'fields': ('inspector_upload_images_text', 'inspector_error', 'inspector_recognize_text',
                       'inspector_report_text', 'inspector_positions_text', 'inspector_report_id')
        }),
    )
    search_fields = ['task__user__email', 'task__task__name', 'task__store__code', 'task__store__address']
    readonly_fields = ['date_start']
    date_hierarchy = 'date_start'
    list_select_related = ('task', 'task__user', 'task__task', 'task__store',)
    raw_id_fields = ('task', )


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):

    list_display = ('date', 'phone', 'code', 'response_code')
    list_display_links = ('date', 'phone', )

    fieldsets = (
        (_('Dates'), {
            'fields': ('date',)
        }),
        (_('Sms'), {
            'fields': ('phone', 'code', 'text')
        }),
        (_('Response'), {
            'fields': ('response_code', 'response_text')
        }),
    )
    search_fields = ['phone', 'code', 'text', 'response_code', 'response_text']
    date_hierarchy = 'date'


@admin.register(StoreTaskAvail)
class StoreTaskAvailAdmin(admin.ModelAdmin):

    list_display = ('store_task_id', 'task_id', 'store_id', 'store_code', 'only_user_id', 'position',
                    'update_time', 'deleted')
    list_display_links = ('store_task_id', )

    fieldsets = (
        (_('Tasks'), {
            'fields': ('store_task_id', 'task_id')
        }),
        (_('Store'), {
            'fields': ('store_id', 'store_code', 'store_client_name', 'store_category_name', 'store_region_id',
                       'store_region_name', 'store_address', 'store_longitude', 'store_latitude')
        }),
        ('Последовательность', {
            'fields': ('position',)
        }),
        (_('User'), {
            'fields': ('only_user_id', 'lock_user_id')
        }),
        (_('Add value'), {
            'fields': ('is_add_value', 'add_value',)
        }),
        (_('Telegram'), {
            'fields': ('telegram_channel_id', )
        }),
        (_('Status'), {
            'fields': ('update_time', 'deleted')
        }),
    )
    search_fields = ('store_task_id', 'task_id', 'store_id', 'store_code', 'store_client_name', 'store_category_name',
                     'store_region_name', 'store_address', 'only_user_id', 'telegram_channel_id')
    list_filter = ('deleted', 'store_region_name', )


@public_model
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )
    search_fields = ['name']


@order_model
@public_model
@admin.register(OutReason)
class OutReasonAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_report', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'is_report', )
        }),
    )
    search_fields = ['name']
    list_filter = ('is_report',)


@admin.register(TasksExecutionCheckInspector)
class TasksExecutionCheckInspectorAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('admin/js/check_v2.js', 'admin/js/fancybox.umd.js')
        css = {
            'all': ('admin/css/fancybox.css',)
        }

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('set-bad-1'):
            te_id = request.GET['set-bad-1']
            try:
                obj = TasksExecution.objects.get(id=te_id)
                obj.status = 5
                obj.comments_status = 'Выкладка товара или фото плохого качества.'
                obj.check = 'checked'
                obj.is_auditor = True
                obj.check_user = request.user
                obj.save(update_fields=['status', 'comments_status', 'check', 'is_auditor', 'check_user'])
                ct = ContentType.objects.get_for_model(TasksExecution)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='[{"changed": {"fields": ["status"]}}]')
                messages.success(request, f'Отправлен отказ "Плохая выкладка или фото" по задаче {obj}.')
            except:
                messages.error(request, 'Задача не найдена')
            updated = request.GET.copy()
            del updated['set-bad-1']
            return redirect(request.path + '?' + urllib.parse.urlencode(updated))

        if request.GET.get('set-bad-2'):
            te_id = request.GET['set-bad-2']
            try:
                obj = TasksExecution.objects.get(id=te_id)
                obj.status = 5
                obj.comments_status = 'Неверно указана причина отсутствия товара: не распознано.'
                obj.check = 'checked'
                obj.is_auditor = True
                obj.check_user = request.user
                obj.save(update_fields=['status', 'comments_status', 'check', 'is_auditor', 'check_user'])
                ct = ContentType.objects.get_for_model(TasksExecution)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='[{"changed": {"fields": ["status"]}}]')
                messages.success(request, f'Отправлен отказ "Неверно указана причина отсутствия товара" по задаче {obj}.')
            except:
                messages.error(request, 'Задача не найдена')
            updated = request.GET.copy()
            del updated['set-bad-2']
            return redirect(request.path + '?' + urllib.parse.urlencode(updated))

        if request.GET.get('set-bad-3'):
            te_id = request.GET['set-bad-3']
            try:
                obj = TasksExecution.objects.get(id=te_id)
                obj.status = 5
                obj.comments_status = 'Нет подтверждения нулевых остатков.'
                obj.check = 'checked'
                obj.is_auditor = True
                obj.check_user = request.user
                obj.save(update_fields=['status', 'comments_status', 'check', 'is_auditor', 'check_user'])
                ct = ContentType.objects.get_for_model(TasksExecution)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='[{"changed": {"fields": ["status"]}}]')
                messages.success(request, f'Отправлен отказ "Нет подтверждения нулевых остатков" по задаче {obj}.')
            except:
                messages.error(request, 'Задача не найдена')
            updated = request.GET.copy()
            del updated['set-bad-3']
            return redirect(request.path + '?' + urllib.parse.urlencode(updated))

        if request.GET.get('set-bad-4'):
            te_id = request.GET['set-bad-4']
            try:
                obj = TasksExecution.objects.get(id=te_id)
                obj.status = 5
                obj.comments_status = 'Нет комментария или фото нулевых остатков.'
                obj.check = 'checked'
                obj.is_auditor = True
                obj.check_user = request.user
                obj.save(update_fields=['status', 'comments_status', 'check', 'is_auditor', 'check_user'])
                ct = ContentType.objects.get_for_model(TasksExecution)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='[{"changed": {"fields": ["status"]}}]')
                messages.success(request, f'Отправлен отказ "Нет комментария или фото нулевых остатков" по задаче {obj}.')
            except:
                messages.error(request, 'Задача не найдена')
            updated = request.GET.copy()
            del updated['set-bad-4']
            return redirect(request.path + '?' + urllib.parse.urlencode(updated))

        if request.GET.get('set-check'):
            te_id = request.GET['set-check']
            try:
                obj = TasksExecution.objects.get(id=te_id)
                obj.status = 3
                obj.check = 'checked'
                obj.is_auditor = True
                obj.check_user = request.user
                obj.save(update_fields=['status', 'check', 'is_auditor', 'check_user'])
                ct = ContentType.objects.get_for_model(TasksExecution)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='[{"changed": {"fields": ["status"]}}]')
                messages.success(request, f'Одобрена задача {obj}.')
            except:
                messages.error(request, 'Задача не найдена')
            updated = request.GET.copy()
            del updated['set-check']
            return redirect(request.path + '?' + urllib.parse.urlencode(updated))

        response = super(TasksExecutionCheckInspectorAdmin, self).changelist_view(request, extra_context)        
        return response

    def get_queryset(self, request):
        out_reasons = TasksExecutionOutReason.objects.filter(task=OuterRef('pk'))
        qs = super(TasksExecutionCheckInspectorAdmin, self).get_queryset(request)
        qs = qs.filter(
            check='not_checked', status__in=[2, 3]
        ).annotate(
            out_reasons_exist=Exists(out_reasons)
        ).filter(out_reasons_exist=True)
        return qs

    def get_check_html(self, obj):

        # Получаем шаг
        step_name = None
        if obj.task is not None:
            step = TaskStep.objects.filter(task=obj.task, photo_out_reason=True).first()
            if step is not None:
                step_name = step.name

        # Изображения выкладки
        images = TasksExecutionImage.objects.filter(task=obj)
        if step_name:
            images = images.filter(constructor_step_name=step_name)

        images_html = '<b style="line-height: 22px; display: block">Фото выкладки:</b><br/>'
        counter = 0
        for image in images:
            counter += 1
            images_html += f'''
            <a href="{image.image.url}" target="_blank">
            <img src="https://admin.shop-survey.ru{image.image.url}" data-fancybox="{obj.id}" 
            data-caption="Фото выкладки {counter}" style="height: 300px" />
            </a> 
            '''

        # Изображения причин не распозналось
        out_reasons_inspector = TasksExecutionOutReason.objects.filter(
            task=obj, out_reason__is_report=True).prefetch_related('good')
        out_reasons = out_reasons_inspector.values_list('good__name', flat=True)
        goods = '&nbsp;&nbsp;' + ', &nbsp;&nbsp;'.join(out_reasons)
        images_html_i = ''
        if out_reasons_inspector.count() > 0:
            images_html_i = f'<span style="line-height: 22px; display: block; padding-top: 16px;"><b>' \
                            f'Не распознались товары:</b> {goods}</span>'
        is_photo = False
        for i in out_reasons_inspector:
            if i.image:
                if not is_photo:
                    is_photo = True
                    images_html_i += '<b style="line-height: 22px; display: block; padding-top: 6px;">' \
                                     'Фото не распознанных товаров:</b><br/>'
                images_html_i += f'''
                <div style="display: inline-block; position: relative">
                <a href="{i.image.url}" target="_blank">
                <img src="https://admin.shop-survey.ru{i.image.url}" data-fancybox="{obj.id}" 
                data-caption="«Не распознался» товар «{i.good.name}»" style="height: 300px" />
                </a> 
                <span style="position: absolute; background: #eaeaea; top: 0; left: 0; z-index: 100">
                На распознался</span>                
                </div>
                '''

        # Изображения причин не другое
        out_reasons_inspector = TasksExecutionOutReason.objects.filter(
            task=obj, out_reason__is_report=False).prefetch_related('good', 'out_reason')
        out_reasons = out_reasons_inspector.values_list('good__name', flat=True)
        goods = '&nbsp;&nbsp;' + ', &nbsp;&nbsp;'.join(out_reasons)
        images_html_o = ''
        if out_reasons_inspector.count() > 0:
            images_html_o = f'<span style="line-height: 22px; display: block; padding-top: 16px;"><b>' \
                            f'Отсутствуют товары:</b> {goods}</span>'
        is_photo = False
        for i in out_reasons_inspector:
            if i.image:
                if not is_photo:
                    is_photo = True
                    images_html_o += '<b style="line-height: 22px; display: block; padding-top: 6px">' \
                                     'Фото товаров нет в наличии:</b><br/>'
                images_html_o += f'''
                <div style="display: inline-block; position: relative">
                <a href="{i.image.url}" target="_blank">
                <img src="https://admin.shop-survey.ru{i.image.url}" style="height: 300px" data-fancybox="{obj.id}" 
                data-caption="«{i.out_reason.name}» товар «{i.good.name}»" />
                </a> 
                <span style="position: absolute; background: #eaeaea; top: 0; left: 0; z-index: 100">
                {i.out_reason.name}</span>
                </div>
                '''

        # Комментарий
        if obj.comments:
            comment = f'<span style="line-height: 22px; display: block; padding: 6px 0;">' \
                      f'<b>Комментарий пользователя:</b> &nbsp;&nbsp;{obj.comments}</span>'
        else:
            comment = ''

        return mark_safe(f'''
        <input type="button" value="Принять" class="default"  onclick="set_check({obj.id})" style="float: none;">
        </td>
        <tr class="row1"><td colspan="10">{comment}{images_html}{images_html_i}{images_html_o}</td></tr>
        <tr class="row1"><td colspan="10" style="background: #dddddd"><br/></td></tr>
        ''')
    get_check_html.allow_tags = True
    get_check_html.short_description = 'Проверка'

    def decline_1_html(self, obj):
        return mark_safe(f'''
        <input type="button" value="Плохая выкладка\nили фото" class="default" onclick="set_bad_1({obj.id})">
        ''')
    decline_1_html.allow_tags = True
    decline_1_html.short_description = 'Отказать'

    def decline_2_html(self, obj):
        return mark_safe(f'''
        <input type="button" value="Неверная причина\nне распозналось" class="default" onclick="set_bad_2({obj.id})">
        ''')
    decline_2_html.allow_tags = True
    decline_2_html.short_description = 'Отказать'

    def decline_3_html(self, obj):
        return mark_safe(f'''
        <input type="button" value="Не нулевые\nостатки" class="default" onclick="set_bad_3({obj.id})">
        ''')
    decline_3_html.allow_tags = True
    decline_3_html.short_description = 'Отказать'

    def decline_4_html(self, obj):
        return mark_safe(f'''
        <input type="button" value="Нет\nкомментария" class="default" onclick="set_bad_4({obj.id})">
        ''')
    decline_4_html.allow_tags = True
    decline_4_html.short_description = 'Отказать'

    def get_status_html(self, obj):
        if obj.status == 1:
            return mark_safe('<span style="color: gray">%s</span>' % obj.get_status_display())
        if obj.status == 3:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_status_display())
        if obj.status == 4:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_status_display())
        if obj.status == 5:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_status_display())
        if obj.status == 6:
            return mark_safe('<b>%s</b>' % obj.get_status_display())
        return obj.get_status_display()
    get_status_html.allow_tags = True
    get_status_html.short_description = _('Status')

    def get_store_html(self, obj):
        return mark_safe('<a href="%s" target=blank>%s</a>' %
                         (reverse('admin:survey_tasksexecution_change', args=[obj.id]), obj.store, ))
    get_store_html.allow_tags = True
    get_store_html.short_description = _('Store')

    list_display = ('user', 'date_start', 'get_store_html', 'task', 'get_status_html', 'decline_1_html',
                    'decline_2_html', 'decline_3_html', 'decline_4_html', 'get_check_html')
    list_display_links = ('user', )

    fieldsets = (
        (None, {
            'fields': ('user', 'store', 'status', 'check', 'date_start', )
        }),
    )
    search_fields = ['task__name', 'user__username', 'user__first_name', 'user__last_name', 'user__telegram_id',
                     'user__phone', 'user__name', 'user__surname', 'user__email', 'store__address', 'comments']
    raw_id_fields = ['user', 'store']
    readonly_fields = ['date_start']
    date_hierarchy = 'date_start'
    list_select_related = ('user', 'store', 'task', 'store__client')
    list_filter = (TaskFilter, ClientFilter, RegionFilter, CodeFilter)
    list_per_page = 10
    inlines = [CheckImageAdmin]


class PenaltyRepaymentInLine(admin.TabularInline):

    model = PenaltyRepayment

    def te_link(self, instance):
        url = reverse('admin:survey_tasksexecution_change',
                      args=(instance.te.id,))
        return format_html(u'<a href="{}">{}</a>', url, instance.te.__str__())

    readonly_fields = ('te_link',)
    fields = ('id', 'te_link', 'repayment_sum',)
    te_link.short_description = 'Выполненная задача'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj):
        return False


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'amount', 'repayment_amount', 'creator', 'date_create', 'description')
    list_display_links = ('id', 'user', )

    readonly_fields = ('repayment_amount', 'creator')
    search_fields = ('user__first_name', 'user__last_name',
                     'user__name', 'user__surname',
                     'user__phone', 'user__email',
                     'creator__first_name', 'creator__last_name',
                     'creator__name', 'creator__surname',
                     'creator__phone', 'creator__email', 'date_create', 'description')
    # list_filter = ('date_create',)
    date_hierarchy = 'date_create'

    inlines = [PenaltyRepaymentInLine, ]

    def get_form(self, request, obj, **kwargs):
        form = super(PenaltyAdmin, self).get_form(request, obj, **kwargs)
        form.__dict__['base_fields']['user'] = forms.ModelChoiceField(
            queryset=User.objects.all(),
            widget=autocomplete.ModelSelect2(url='/survey/autocomplete/users/'),
            label='Сюрвеер'
        )
        return form

    def save_model(self, request, obj, form, change):
        """
        Метод создания штрафа и его начального погашения суммой стоимости задач te со статусом 3,
        имеющихся у пользователя.
        """

        obj.creator = request.user
        obj.save()

        # tasks = TasksExecution.objects.filter(
        #     user__id=obj.user.id,
        #     status=3,
        #     money__gt=0,
        #     date_start__gt=datetime.datetime.now()
        # ).all()
        #
        # if obj.amount > 0 and not PenaltyRepayment.objects.filter(penalty=obj).all():
        #     penalty_repayment_list = []
        #     with transaction.atomic():
        #         obj.creator = User.objects.get(email=request.user)
        #         obj.save()
        #         i = 0
        #         len_tasks = len(tasks)
        #         while obj.repayment_amount < obj.amount and i < len_tasks:
        #             task = tasks[i]
        #             if obj.repayment_amount + task.money > obj.amount:
        #                 repayment_sum = obj.amount - obj.repayment_amount
        #                 obj.repayment_amount = obj.amount
        #             else:
        #                 obj.repayment_amount = obj.repayment_amount + task.money
        #                 repayment_sum = task.money
        #             penalty_repayment_list.append(PenaltyRepayment(penalty=obj, te=task,
        #                                                            repayment_sum=round(repayment_sum, 1)))
        #             task.money = round(task.money - repayment_sum, 1)
        #             i += 1
        #         obj.save()
        #         PenaltyRepayment.objects.bulk_create(penalty_repayment_list)
        #         TasksExecution.objects.bulk_update(tasks, ['money'])

    def delete_model(self, request, obj):
        """
        Метод удаления штрафа с полным откатом погашения по кнопке "Удаление".
        """
        repayments = PenaltyRepayment.objects.filter(penalty=obj).all()
        back_task_list = [TasksExecution(
            id=repayment.te.id, money=round(repayment.te.money + repayment.repayment_sum, 1)
        ) for repayment in repayments]
        with transaction.atomic():
            obj.delete()
            TasksExecution.objects.bulk_update(back_task_list, ['money'])

    def delete_queryset(self, request, queryset):
        """
        Метод удаления штрафов с полным откатом погашения по действию "Удалить выделенные"
        """
        back_task_list = []
        for penalty in queryset:
            repayments = PenaltyRepayment.objects.filter(penalty=penalty).all()
            back_task_list.extend([TasksExecution(
                id=repayment.te.id, money=round(repayment.te.money + repayment.repayment_sum, 1)
            ) for repayment in repayments])
        with transaction.atomic():
            queryset.delete()
            TasksExecution.objects.bulk_update(back_task_list, ['money', ])
