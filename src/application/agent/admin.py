from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export.formats.base_formats import DEFAULT_FORMATS, XLSX, CSV

from public_model.admin import public_model
from sort_model.admin import order_model

from .models import Category, Brand, Good, Import, Store, Order, OrderGood, City, Schedule, Payment, StoreCategory, \
    GoodPriceType, PromoCode, TinkoffPayment
from .resources import OrderResource, StoreResource, PromoCodeResource, StoreImportResource


@public_model
@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = ('name', 'code', 'source', 'email', )
    list_display_links = ('name', 'code', )

    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'source', 'email', )
        }),
    )
    search_fields = ['name', 'code', 'source', 'email']


@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'default', 'payment_name', 'telegram_channel_id', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'default', )
        }),
        (_('Payment'), {
            'fields': ('payment_name', 'payment_string',)
        }),
        (_('Telegram'), {
            'fields': ('telegram_channel_id',)
        }),
    )
    search_fields = ['name', 'payment_name', 'payment_string', 'telegram_channel_id']
    list_filter = ('default',)


@public_model
@order_model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super(CategoryAdmin, self).get_queryset(request).prefetch_related('store_categories')

    list_display = ('name', 'get_store_categories', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        (_('Visibility'), {
            'fields': ('store_categories', )
        }),
    )
    search_fields = ['name', 'store_categories__name']
    list_filter = ('store_categories', )
    filter_horizontal = ('store_categories',)


@public_model
@order_model
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ('name', 'cashback_percent')
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'cashback_percent')
        }),
    )
    search_fields = ['name', 'cashback_percent']


class GoodPriceTabularInlineAdmin (admin.TabularInline):

    model = GoodPriceType
    fields = ('price_type', 'price')
    extra = 0


@public_model
@order_model
@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super(GoodAdmin, self).get_queryset(request).prefetch_related('categories')

    list_display = ('code', 'name', 'get_categories', 'brand', 'unit', 'price', 'box_count', 'min_count', 'rest',
                    'is_not_delete', 'is_no_order', )
    list_display_links = ('code', 'name', )

    fieldsets = (
        (None, {
            'fields': ('code', 'name', )
        }),
        (_('Category'), {
            'fields': ('brand', 'categories', 'manufacturer', 'brand_name', )
        }),
        (_('Price'), {
            'fields': ('unit', 'box_count', 'min_count', 'price', 'rest', 'cashback', )
        }),
        (_('Description'), {
            'fields': ('description', 'image', 'url',)
        }),
        (_('Flags'), {
            'fields': ('is_not_delete', 'is_no_order', 'is_only_text', )
        }),
    )
    search_fields = ['name', 'code', 'brand__name', 'unit', 'manufacturer', 'brand_name']
    # list_filter = ('is_popular', 'is_oeskimo', 'brand', 'category', 'categories', )
    list_filter = ('brand', 'categories', 'is_not_delete', 'is_no_order', 'is_only_text', 'manufacturer',
                   'brand_name', )
    list_select_related = ('brand', 'category', )
    inlines = [GoodPriceTabularInlineAdmin, ]
    list_per_page = 40
    filter_horizontal = ('categories', )


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):

    list_display = ('file_name', 'date_start', 'date_end', 'rows_count', 'rows_process', 'status')
    list_display_links = ('file_name', 'date_start', )

    fieldsets = (
        (None, {
            'fields': ('file_name', 'rows_count', 'rows_process', 'status', 'report_text', )
        }),
        (_('Dates'), {
            'fields': ('date_start', 'date_end', )
        }),
    )
    search_fields = ['file_name']
    date_hierarchy = 'date_start'
    readonly_fields = ('date_start',)
    list_filter = ('status',)


@admin.register(Store)
class StoreAdmin(ImportExportMixin, admin.ModelAdmin):

    def get_import_resource_class(self):
        return StoreImportResource

    def address_short(self, obj):
        s = str(obj.address)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    address_short.short_description = _('Address')

    def user_advisor(self, obj):
        return obj.user.advisor
    user_advisor.short_description = _('Advisor')

    list_display = ('date_create', 'user', 'user_advisor', 'name', 'inn', 'city', 'address_short',
                    'category', 'stock')
    list_display_links = ('date_create', 'name', )

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'contact', 'phone', 'inn', 'city', 'address', 'agent', 'stock')
        }),
        (_('Agreement'), {
            'fields': ('is_agreement',)
        }),
        (_('Category'), {
            'fields': ('category', )
        }),
        (_('Dates'), {
            'fields': ('date_create', )
        }),
        (_('External data'), {
            'fields': ('inn_name', 'inn_full_name', 'inn_director_title', 'inn_director_name', 'inn_address',
                       'inn_kpp', 'inn_ogrn', 'inn_okved', 'inn_region')
        }),
        (_('Loyalty'), {
            'fields': ('loyalty_department', 'loyalty_program', 'loyalty_1c_code', 'loyalty_1c_user', )
        }),
        (_('1с values'), {
            'fields': ('loyalty_plan', 'loyalty_fact', 'loyalty_cashback', 'loyalty_sumcashback',
                       'loyalty_cashback_payed', 'loyalty_cashback_to_pay', 'loyalty_debt', 'loyalty_overdue_debt',
                       'price_type', )
        }),
        (_('Flags'), {
            'fields': ('is_deleted', )
        }),
    )
    search_fields = ['user__last_name', 'user__first_name', 'user__username', 'user__advisor', 'name', 'contact',
                     'phone', 'address', 'inn', 'user__email', 'city__name', 'city__code', 'loyalty_1c_code',
                     'loyalty_department__name', 'loyalty_program__name', 'agent', 'category__name', 'price_type',
                     'inn_region']
    date_hierarchy = 'date_create'
    readonly_fields = ('date_create',)
    raw_id_fields = ('user', )
    list_select_related = ('user', 'city', 'loyalty_department', 'loyalty_program', 'category', 'user__status',
                           'user__status_agent', 'stock')
    list_filter = ('is_agreement', 'category', 'city', 'stock', 'inn_region', 'loyalty_department', 'loyalty_program')
    resource_class = StoreResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)


class OrderGoodInlineTabularAdmin (admin.StackedInline):

    model = OrderGood
    fields = ('count', 'code', 'name', 'category', 'brand', 'unit', 'price', 'sum', 'good_source')
    extra = 0
    list_select_related = ('category', 'brand', 'good_source')
    raw_id_fields = ('good_source', )


class OrderAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(OrderAdminForm, self).clean()
        if self.cleaned_data.get('status', None) == 3 and self.request.user.email not in settings.SOLAR_STAFF_USERS:
            raise ValidationError({
                'status': _('You do not have rights to set this status.')
            })
        return cleaned_data


def set_status_pay_solar(modeladmin, request, queryset):
    if request.user.email in settings.SOLAR_STAFF_USERS:
        c = queryset.count()
        for i in queryset:
            i.status = 3
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


def set_status_payed(modeladmin, request, queryset):
    c = queryset.count()
    queryset.update(status=2)
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


set_status_payed.short_description = _('Mark selected item status payed')


def set_status_finished(modeladmin, request, queryset):
    c = queryset.count()
    queryset.update(status=5)
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


set_status_finished.short_description = _('Mark selected item status finished')


def calc_cashback(modeladmin, request, queryset):
    c = queryset.count()
    for i in queryset:
        i.calc_cashback()
        i.save()
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message='[{"changed": {"fields": ["cashback_sum"]}}]')
    modeladmin.message_user(request, _('%s items was calc cashback') % c)


calc_cashback.short_description = _('Calc cashback selected items')


@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):

        AdminForm = super(OrderAdmin, self).get_form(request, obj, **kwargs)

        class OrderRequestAdminForm(AdminForm):

            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return OrderRequestAdminForm

    def get_status_html(self, obj):
        if obj.status == 1:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_status_display())
        if obj.status == 2:
            return mark_safe('<span style="">%s</span>' % obj.get_status_display())
        if obj.status == 5:
            return mark_safe('<b style="color: green">%s</b>' % obj.get_status_display())
        if obj.status == 6:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_status_display())
        if obj.status == 4:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_status_display())
        if obj.status == 7:
            return mark_safe('<span style="color: red"><b>%s</b></span>' % obj.get_status_display())
        if obj.status == 3:
            return mark_safe('<b>%s</b>' % obj.get_status_display())
        return obj.get_status_display()
    get_status_html.allow_tags = True
    get_status_html.short_description = _('Status')

    def get_inn(self, obj):
        if obj.store:
            return obj.store.inn
        return '-'
    get_inn.short_description = _('Inn')

    def get_city(self, obj):
        if obj.store:
            return obj.store.city
        return '-'
    get_city.short_description = _('City')

    def get_advisor(self, obj):
        if obj.user:
            return obj.user.advisor
        return '-'
    get_advisor.short_description = _('Advisor')

    def get_category(self, obj):
        if obj.store:
            return obj.store.category
        return '-'
    get_category.short_description = _('Category')

    def get_store(self, obj):
        if obj.store:
            s = str(obj.store)
            return s
        return '-'
    get_store.short_description = _('Store')

    list_display = ('id', 'date_order', 'user', 'get_store', 'get_city', 'get_category', 'get_advisor', 'delivery_date',
                    'sum', 'cashback_sum', 'need_check', 'get_status_html', 'from_1c_sum', 'from_1c_pay')
    list_display_links = ('id', 'date_order', )

    fieldsets = (
        (None, {
            'fields': ('user', 'store', 'get_inn', 'comment', 'need_check', )
        }),
        (_('Dates'), {
            'fields': ('date_order', )
        }),
        (_('Delivery'), {
            'fields': ('delivery_date', 'delivery_address')
        }),
        (_('Sum'), {
            'fields': ('sum', 'cashback_sum', 'calc_cashback_sum')
        }),
        (_('Status change'), {
            'fields': ('status', 'comments_status')
        }),
        (_('1c data'), {
            'fields': ('from_1c_firm', 'from_1c_sum', 'from_1c_pay', 'from_1c_status', )
        }),
        (_('Payment'), {
            'fields': ('payment_type', 'payment_status', 'payment_sum', )
        }),
        (_('Solar Staff'), {
            'fields': ('ss_account', )
        }),
    )
    search_fields = ['user__last_name', 'user__first_name', 'user__username', 'comment', 'delivery_address',
                     'user__email', 'user__advisor', 'store__name', 'store__inn', 'store__phone', 'id', 'from_1c_firm']
    date_hierarchy = 'date_order'
    readonly_fields = ('date_order', 'get_inn',)
    raw_id_fields = ('user', 'store')
    list_select_related = ('user', 'store', 'store__city', 'ss_account', 'store__category')
    inlines = [OrderGoodInlineTabularAdmin, ]
    list_filter = ('status', 'need_check', 'store__city', 'store__category', 'from_1c_status', 'ss_account',
                   'payment_type', 'payment_status', )
    form = OrderAdminForm
    actions = [set_status_pay_solar, set_status_payed, set_status_finished, calc_cashback]
    resource_class = OrderResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)


@public_model
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    def get_readonly_fields(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return 'date_create',
        else:
            return 'date_create', 'source', 'provider', 'total_amount', 'currency', 'invoice_payload', \
                   'telegram_payment_charge_id', 'provider_payment_charge_id'

    list_display = ('date_create', 'source', 'provider', 'total_amount', 'invoice_payload', )
    list_display_links = ('date_create', )

    fieldsets = (
        (None, {
            'fields': ('date_create', )
        }),
        (_('Payment type'), {
            'fields': ('source', 'provider', )
        }),
        (_('Payment info'), {
            'fields': ('total_amount', 'currency', 'invoice_payload', )
        }),
        (_('System info'), {
            'fields': ('telegram_payment_charge_id', 'provider_payment_charge_id',)
        }),
    )
    search_fields = ['source', 'provider', 'invoice_payload', 'currency']
    list_filter = ('source', 'provider', 'currency', )
    date_hierarchy = 'date_create'
    readonly_fields = ('date_create', 'source', 'provider', 'total_amount', 'currency', 'invoice_payload',
                       'telegram_payment_charge_id', 'provider_payment_charge_id')


@admin.register(PromoCode)
class PromoCodeAdmin(ImportMixin, admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.email in settings.PROMO_CODES_USERS:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.email in settings.PROMO_CODES_USERS:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.email in settings.PROMO_CODES_USERS:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.email in settings.PROMO_CODES_USERS:
            return True
        return False

    list_display = ('code', 'is_used', 'store', )
    list_display_links = ('code', )

    fieldsets = (
        (None, {
            'fields': ('code', 'store', 'is_used', )
        }),
    )
    search_fields = ['code', 'store__name', 'store__phone', 'store__address', 'store__inn', 'store__loyalty_1c_code']
    raw_id_fields = ('store', )
    list_select_related = ('store', )
    resource_class = PromoCodeResource
    formats = (CSV, )


@admin.register(TinkoffPayment)
class TinkoffPaymentAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    def has_change_permission(self, request, obj=None):
        if request.user.email == settings.AUTH_USER_DEVELOPER:
            return True
        return settings.DEBUG

    list_display = ('date_create', 'terminal_key', 'order_id', 'status', 'amount', 'success', )
    list_display_links = ('date_create', )

    fieldsets = (
        (None, {
            'fields': ('date_create', 'terminal_key', 'order_id', 'payment_id', 'error_code',
                       'amount', 'card_id', 'pan', 'exp_date', 'status', 'success')
        }),
    )
    search_fields = ['source', 'provider', 'invoice_payload', 'currency']
    list_filter = ('status', 'success', )
    date_hierarchy = 'date_create'
    readonly_fields = ('date_create', )
