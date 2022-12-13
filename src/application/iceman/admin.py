from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from import_export.formats.base_formats import DEFAULT_FORMATS, XLSX
from public_model.admin import public_model
from sort_model.admin import order_model, order_model_inline

from .models import Notification, Source, Stock, Store, StoreStock, Brand, Category, Product, ProductStock, Order, \
    OrderProduct, StoreTask, Region, StoreDocument, SourceProduct, SourceProductPrice, StoreTaskSchedule, Document, \
    DocumentGroup, DocumentGroupDocument
from .resources import OrderResource


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


@admin.register(Region)
class RegionAdmin (admin.ModelAdmin):

    list_display = ('name', 'short_name', 'short_name_2', 'name_1c', 'name_1c_2', 'source', 'stock', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'short_name', 'short_name_2', 'name_1c', 'name_1c_2', )
        }),
        ('Связи', {
            'fields': ('stock', 'source',)
        }),
    )

    raw_id_fields = ['stock']
    list_select_related = ('source', 'stock')
    search_fields = ('name', 'short_name', 'short_name_2', 'stock__name', 'name_1c', 'name_1c_2', 'source__name')


@admin.register(Source)
class SourceAdmin (admin.ModelAdmin):

    list_display = ('name', 'sys_name', 'bonus', 'discount', 'sum_restrict', 'delivery_max_days', 'worker_bonus')
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name',)
        }),
        ('Настройка', {
            'fields': ('bonus', 'worker_bonus', 'delivery_max_days')
        }),
        ('Оплата по факту', {
            'fields': ('discount', 'fact_text')
        }),
        ('Отсрочка', {
            'fields': ('sum_restrict', 'payment_days', 'delay_text')
        }),
        ('Связь', {
            'fields': ('email', 'telegram_id', 'go_telegram_id')
        }),
        ('Данные партнера', {
            'fields': ('partner_name', 'partner_email', 'partner_fio', 'partner_phone')
        }),
    )

    search_fields = ('name', 'sys_name', 'email', 'partner_name', 'partner_email', 'partner_fio', 'partner_phone',
                     'telegram_id')


@admin.register(Stock)
class StockAdmin (admin.ModelAdmin):

    list_display = ('name', 'sys_name', 'source', 'default')
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name', 'source', )
        }),
        (_('Flags'), {
            'fields': ('default', )
        }),
    )

    search_fields = ('name', 'sys_name', )
    list_filter = ('default', 'source', )


class StoreStockInlineAdmin (admin.TabularInline):

    model = StoreStock
    fields = ('stock', )
    extra = 0
    list_select_related = ('stock', )
    raw_id_fields = ('stock', )


class StoreDocumentInlineAdmin (admin.TabularInline):

    model = StoreDocument
    fields = ('date_create', 'type', 'document', 'number', 'file', 'user')
    extra = 0
    raw_id_fields = ('user', )
    readonly_fields = ('date_create', )


@public_model
@admin.register(Store)
class StoreAdmin (admin.ModelAdmin):

    def short_address(self, obj):
        s = str(obj.address)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    short_address.short_description = _('Address')

    list_display = ('name', 'code', 'source', 'region', 'short_address', 'is_agreement', 'is_agreement_data',
                    'date_create', 'is_order_task', 'type', )
    list_display_links = ('name', 'code', )

    fieldsets = (
        (None, {
            'fields': ('source', 'type', 'date_create', 'user', )
        }),
        ('Название', {
            'fields': ('name', 'code')
        }),
        (_('Geo location'), {
            'fields': ('region', 'address', 'longitude', 'latitude', 'auto_coord')
        }),
        ('Данные по ИНН', {
            'fields': ('inn', 'inn_name', 'inn_name_1', 'inn_director_title', 'inn_director_name',
                       'inn_address', 'inn_kpp', 'inn_ogrn', 'inn_okved', 'inn_type', 'inn_region', 'inn_auto')
        }),
        (_('Flags'), {
            'fields': ('is_agreement', 'is_agreement_data', )
        }),
        ('Контакты', {
            'fields': ('lpr_phone', 'lpr_fio', 'director_phone', 'director_fio', )
        }),
        ('Продажи', {
            'fields': ('is_order_task', 'schedule', 'price_type', 'payment_days', 'sum_restrict', 'is_entry',)
        }),
        ('Фото', {
            'fields': ('photo',)
        }),
    )

    search_fields = ('name', 'code', 'address', 'inn', 'inn_name', 'inn_name_1', 'inn_director_title',
                     'inn_director_name', 'inn_address', 'inn_kpp', 'inn_ogrn', 'inn_okved', 'inn_type',
                     'lpr_phone', 'lpr_fio', 'director_phone', 'director_fio', 'price_type', 'region__name',
                     'inn_region', 'user__email')
    list_select_related = ('source', 'region', )
    list_filter = ('source', 'type', 'is_agreement', 'is_agreement_data', 'is_order_task', 'is_entry', )
    inlines = (StoreStockInlineAdmin, StoreDocumentInlineAdmin)
    raw_id_fields = ('user',)
    date_hierarchy = 'date_create'


@public_model
@order_model
@admin.register(Brand)
class BrandAdmin (admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    search_fields = ('name', )


@public_model
@order_model
@admin.register(Category)
class CategoryAdmin (admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    search_fields = ('name', )


class ProductStockInlineAdmin(admin.TabularInline):

    model = ProductStock
    fields = ('stock', 'count', )
    extra = 0
    list_select_related = ('stock', )
    raw_id_fields = ('stock', )


@public_model
@order_model
@admin.register(Product)
class ProductAdmin (admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('categories')

    def html_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 75px; border-radius: 8px;" alt=""/>')
        else:
            return ''
    html_image.short_description = _('Image')
    html_image.allow_tags = True

    list_display = ('html_image', 'name', 'code', 'brand', 'get_categories', 'price', 'barcode', 'weight', )
    list_display_links = ('html_image', 'name', 'code', )

    fieldsets = (
        (None, {
            'fields': ('name', 'code', )
        }),
        ('Контент', {
            'fields': ('description', 'image', 'barcode', 'weight',)
        }),
        ('Раздел', {
            'fields': ('categories', 'brand',)
        }),
        ('Продажа', {
            'fields': ('price', 'unit', 'box_count', 'min_count',)
        }),
    )

    search_fields = ('name', 'code', )
    list_select_related = ('brand', )
    list_filter = ('brand', 'categories', )
    filter_horizontal = ('categories', )
    inlines = (ProductStockInlineAdmin, )


class OrderProductInlineAdmin (admin.StackedInline):

    model = OrderProduct
    fields = ('product', 'code', 'barcode', 'name', 'brand_name', 'weight', 'unit', 'box_count', 'count', 'price_one',
              'price', 'is_bonus')
    extra = 0
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin (ExportMixin, admin.ModelAdmin):

    def status_html(self, obj):
        if obj.status == 1:
            return mark_safe(f'<span style="color: blue">{obj.get_status_display()}</span>')
        if obj.status == 2:
            return mark_safe(f'<span style="color: red">{obj.get_status_display()}</span>')
        if obj.status == 3:
            return mark_safe(f'<span style="color: green">{obj.get_status_display()}</span>')
        if obj.status == 4:
            return mark_safe(f'<span style="color: grey">{obj.get_status_display()}</span>')
        if obj.status == 5:
            return mark_safe(f'<span style="color: #000; font-weight: bold;">{obj.get_status_display()}</span>')
        return obj.get_status_display()
    status_html.allow_tags = True
    status_html.short_description = 'Статус'

    def task_link_html(self, obj):
        if obj.task_id is None:
            return '-'
        return mark_safe(f'<a href="/survey/tasksexecution/{obj.task_id}/" '
                         f'target="_blank">https://admin.shop-survey.ru/survey/tasksexecution/{obj.task_id}/</a>')
    task_link_html.allow_tags = True
    task_link_html.short_description = 'Ссылка на задачу'

    def store_name(self, obj):
        if obj.store is None:
            return '-'
        return str(obj.store)
    store_name.allow_tags = True
    store_name.short_description = 'Магазин'

    def user_status(self, obj):
        if obj.user is None:
            return '-'
        return str(obj.user.get_status_legal_display())
    user_status.allow_tags = True
    user_status.short_description = 'Статус'

    def task_status_html(self, obj):
        if obj.task_status is None:
            return '-'
        if obj.task_status == 1:
            return mark_safe('<span style="color: gray">%s</span>' % obj.get_task_status_display())
        if obj.task_status == 3:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_task_status_display())
        if obj.task_status == 4:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_task_status_display())
        if obj.task_status == 5:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_task_status_display())
        if obj.task_status == 6:
            return mark_safe('<b>%s</b>' % obj.get_task_status_display())
        return str(obj.get_task_status_display())
    task_status_html.allow_tags = True
    task_status_html.short_description = 'Статус задачи'

    def user_html(self, obj):
        if obj.user is None:
            return '-'
        return mark_safe(obj.user)
    user_html.allow_tags = True
    user_html.short_description = 'Пользователь'

    list_display = ('order_id', 'date_create', 'delivery_date', 'user_html', 'store_name',
                    'payment_type', 'price', 'payment_sum_correct', 'payment_sum', 'debt_sum', 'days_overdue',
                    'payment_sum_user', 'type', 'task_status_html', 'status_html', )
    list_display_links = ('order_id', 'date_create', )

    fieldsets = (
        (None, {
            'fields': ('order_id', 'date_create', 'status', 'type', )
        }),
        ('Принадлежность', {
            'fields': ('user', 'user_money', 'store', 'task_id', 'task_link_html', 'source', )
        }),
        ('Данные заказа', {
            'fields': ('delivery_address', 'delivery_date', 'comment')
        }),
        (_('Payment'), {
            'fields': ('price', 'price_type', 'payment_type', 'payment_method', 'payment_sum_correct',
                       'payment_sum', 'payment_days', 'payment_sum_user', 'payment_courier', 'payment_url')
        }),
        ('Синхронизация', {
            'fields': ('sync_1c', 'sync_1c_date')
        }),
        ('Оплата черз Тиньков', {
            'classes': ('collapse',),
            'fields': ('payment_phone', 'online_payment_id', 'online_payment_status', 'online_payment_sum',
                       'online_payment_url', 'online_payment_qr_url', 'online_payment_qr_file', 'online_payment_qr',
                       'online_payment_result', 'online_payment_qr_result', 'payment_status')
        }),
        (_('Settings'), {
            'fields': ('email_status', 'telegram_status', )
        }),
    )

    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'user__telegram_id', 'user__phone',
                     'user__name', 'user__surname', 'user__email', 'store__address', 'store__name', 'store__inn',
                     'comment', 'delivery_address', 'task_id')
    readonly_fields = ('order_id', 'date_create', 'task_link_html', 'sync_1c_date')
    raw_id_fields = ['user', 'user_money', 'store']
    list_select_related = ('store', 'user', 'source', 'store__region', )
    list_filter = ('source', 'type', 'status', 'task_status', 'payment_type', 'payment_method', 'sync_1c', )
    inlines = (OrderProductInlineAdmin, )
    date_hierarchy = 'date_create'
    list_per_page = 50
    resource_class = OrderResource
    formats = list(DEFAULT_FORMATS)
    formats.remove(XLSX)


@admin.register(StoreTask)
class StoreTaskAdmin (admin.ModelAdmin):

    list_display = ('id', 'store', 'region', 'task', 'only_user_id', 'lock_user_id', 'days_of_week', 'completed',
                    'done', 'update_time')
    list_display_links = ('id', 'store', 'task', )

    fieldsets = (
        (None, {
            'fields': ('id', 'store', 'region', 'task', 'days_of_week', )
        }),
        (_('User'), {
            'fields': ('only_user_id', 'lock_user_id', )
        }),
        (_('Flags'), {
            'fields': ('completed', 'done', )
        }),
        (_('Dates'), {
            'fields': ('update_time',)
        }),
    )

    search_fields = ('store__address', 'store__name', 'store__inn', 'task__name', 'lock_user_id', 'region__name')
    raw_id_fields = ('store', 'task', 'region')
    list_select_related = ('store', 'task', 'region', )
    list_filter = ('completed', )
    readonly_fields = ('id', 'update_time',)


class SourceProductPriceInlineAdmin(admin.TabularInline):

    model = SourceProductPrice
    fields = ('price_type', 'price', )
    extra = 0


@public_model
@order_model
@admin.register(SourceProduct)
class SourceProductAdmin (admin.ModelAdmin):

    list_display = ('source', 'product', 'price', 'is_bonus', )
    list_display_links = ('source', 'product', )

    fieldsets = (
        (None, {
            'fields': ('source', 'product', )
        }),
        ('Продажа', {
            'fields': ('price', 'unit', 'box_count', 'min_count',)
        }),
        (_('Flags'), {
            'fields': ('is_bonus', )
        }),
    )

    search_fields = ('product__name', 'product__code', )
    list_select_related = ('source', 'product', 'product__brand', )
    list_filter = ('source', 'is_bonus', )
    inlines = (SourceProductPriceInlineAdmin, )
    raw_id_fields = ('product', )


@admin.register(StoreTaskSchedule)
class StoreTaskScheduleAdmin (admin.ModelAdmin):

    list_display = ('task', 'store', 'per_week', 'per_month', 'days_of_week', 'is_once', 'only_user', )
    list_display_links = ('task', 'store')

    fieldsets = (
        (None, {
            'fields': ('task', 'store', )
        }),
        ('Расписание (выбрать одно)', {
            'fields': ('per_week', 'per_month', 'days_of_week', 'is_once', )
        }),
        ('Связи', {
            'fields': ('only_user',)
        }),
    )

    raw_id_fields = ['task', 'store', 'only_user']
    list_select_related = ('task', 'store', 'only_user')
    search_fields = ('task__name', 'store__name', 'store__code', 'store__address', 'only_user__email')


@admin.register(Document)
class DocumentAdmin (admin.ModelAdmin):

    list_display = ('name', 'sys_name', )
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name', 'description', )
        }),
    )

    search_fields = ('name', 'sys_name', 'description', )


@order_model_inline
class DocumentGroupDocumentInlineAdmin(admin.TabularInline):

    model = DocumentGroupDocument
    fields = ('document', 'required', 'is_public', )
    extra = 0


@admin.register(DocumentGroup)
class DocumentGroupAdmin (admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('name', 'sys_name', )
    list_display_links = ('name', 'sys_name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sys_name', )
        }),
    )

    search_fields = ('name', 'sys_name', )
    inlines = (DocumentGroupDocumentInlineAdmin, )
