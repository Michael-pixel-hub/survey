from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import ImportStores, ImportProducts, ImportTasks, UploadRequest


@admin.register(ImportStores)
class ImportStoresAdmin(admin.ModelAdmin):

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


@admin.register(ImportProducts)
class ImportProductsAdmin(admin.ModelAdmin):

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


@admin.register(ImportTasks)
class ImportTasksAdmin(admin.ModelAdmin):

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


@admin.register(UploadRequest)
class UploadRequestsAdmin(admin.ModelAdmin):

    def result_short(self, obj):
        s = str(obj.result)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    result_short.short_description = _('Result')

    list_display = ('request_date', 'request_ip', 'request_method', 'user', 'request_type', 'request_data_type',
                    'result_short', 'request_data_count', 'processed',)
    list_display_links = ('request_date', 'request_ip', 'request_method', )

    fieldsets = (
        (None, {
            'fields': ('request_date', 'request_ip', 'request_method', 'request_type', 'request_text',
                       'request_files', 'user', 'processed', 'request_data_type', 'request_data_count', 'result', )
        }),
    )
    search_fields = ['request_ip', 'request_method', 'request_type', 'request_text', 'request_files', 'result',
                     'request_data_type', 'user__email']
    readonly_fields = ['request_date']
    date_hierarchy = 'request_date'
    list_filter = ('processed', 'request_data_type',)
