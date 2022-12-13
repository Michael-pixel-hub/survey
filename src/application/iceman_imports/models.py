from application.survey.models import User, Task
from application.users.models import User as DjangoUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel
from sort_model.models import OrderModel


class ImportStores(models.Model):

    statuses = (
        (1, _('In process')),
        (2, _('Finished')),
        (3, _('Canceled')),
        (4, _('Error')),
    )

    file_name = models.CharField(_('File name'), max_length=255)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)

    rows_count = models.IntegerField(_('Rows count'), null=True, blank=True)
    rows_process = models.IntegerField(_('Rows process'), blank=True, default=0)

    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    report_text = models.TextField(_('Report text'), null=True, blank=True)

    user = models.ForeignKey(DjangoUser, related_name='iceman_stores_import_user', verbose_name=_('User'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(_('File'), upload_to='imports/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'iceman_imports_stores'
        ordering = ['-date_start']
        verbose_name = _('Store import')
        verbose_name_plural = _('Stores imports')

    def __str__(self):
        return '%s' % self.date_start


class ImportProducts(models.Model):

    statuses = (
        (1, _('In process')),
        (2, _('Finished')),
        (3, _('Canceled')),
        (4, _('Error')),
    )

    file_name = models.CharField(_('File name'), max_length=255)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)

    rows_count = models.IntegerField(_('Rows count'), null=True, blank=True)
    rows_process = models.IntegerField(_('Rows process'), blank=True, default=0)

    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    report_text = models.TextField(_('Report text'), null=True, blank=True)

    user = models.ForeignKey(DjangoUser, related_name='iceman_products_import_user', verbose_name=_('User'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(_('File'), upload_to='imports/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'iceman_imports_products'
        ordering = ['-date_start']
        verbose_name = _('Product import')
        verbose_name_plural = _('Products imports')

    def __str__(self):
        return '%s' % self.date_start


class ImportTasks(models.Model):

    statuses = (
        (1, _('In process')),
        (2, _('Finished')),
        (3, _('Canceled')),
        (4, _('Error')),
    )

    file_name = models.CharField(_('File name'), max_length=255)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)

    rows_count = models.IntegerField(_('Rows count'), null=True, blank=True)
    rows_process = models.IntegerField(_('Rows process'), blank=True, default=0)

    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    report_text = models.TextField(_('Report text'), null=True, blank=True)

    user = models.ForeignKey(DjangoUser, related_name='iceman_tasks_import_user', verbose_name=_('User'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(_('File'), upload_to='imports/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'iceman_imports_tasks'
        ordering = ['-date_start']
        verbose_name = _('Task import')
        verbose_name_plural = _('Tasks imports')

    def __str__(self):
        return '%s' % self.date_start


class UploadRequest(models.Model):

    request_date = models.DateTimeField(_('Request date'), auto_now_add=True)
    request_method = models.CharField(_('Request method'), blank=True, default='', max_length=1000)
    request_type = models.CharField(_('Request type'), blank=True, default='', max_length=1000)
    request_ip = models.CharField(_('Request ip'), blank=True, default='', max_length=1000)
    request_text = models.TextField(_('Request text'), blank=True, default='')
    request_files = models.TextField(_('Request files'), blank=True, default='')

    request_data_type = models.CharField(_('Request data type'), blank=True, default='', max_length=100)
    request_data_count = models.IntegerField(_('Request data count'), blank=True, null=True)

    processed = models.BooleanField(_('Processed'), default=False)
    result = models.TextField(_('Result'), blank=True, default='')

    user = models.ForeignKey(DjangoUser, related_name='iceman_upload_requests_user', verbose_name=_('User'),
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'iceman_1c_requests'
        ordering = ['-request_date']
        verbose_name = '1с запрос айсмен'
        verbose_name_plural = '1с запросы айсмен'

    def __str__(self):
        return '%s %s %s' % (self.request_date, self.request_method, self.request_ip)
