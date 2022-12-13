from django.db import models
from django.utils.translation import ugettext_lazy as _

from application.survey.models import Client, Store, Region

from cache_model.models import CacheModel
from public_model.models import PublicModel
from sort_model.models import OrderModel


SHORT_VALUE_LENGTH = 100


per_weeks = (
    (0, _('Not limited')),
    (1, _('Once a week')),
    (2, _('2 times per week')),
    (3, _('3 times per week')),
    (4, _('4 times per week')),
    (5, _('5 times per week')),
    (6, _('6 times per week')),
)


class User(models.Model):
    """
    Модель пользователей телеграм
    """

    telegram_id = models.IntegerField(_('Telegram id'), unique=True, null=True, blank=True)
    telegram_language_code = models.CharField(_('Language'), max_length=10, blank=True, null=True)
    telegram_last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    telegram_first_name = models.CharField(_('First name'), max_length=255, blank=True, null=True)
    telegram_username = models.CharField(_('Telegram username'), max_length=255, blank=True, null=True)

    is_telegram = models.BooleanField(_('Is telegram'), default=True)
    is_register = models.BooleanField(_('Is register'), default=False)

    company_name = models.CharField(_('Company name'), max_length=100, blank=True, null=True)
    company_inn = models.CharField(_('Company INN'), max_length=100, blank=True, null=True)

    fio = models.CharField(_('FIO'), max_length=200, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=100, blank=True, null=True)
    email = models.CharField(_('E-mail'), blank=True, null=True, max_length=100)

    date_join = models.DateTimeField(_('Date join'), auto_now_add=True)

    is_manager = models.BooleanField(_('Is manager'), default=False)

    class Meta:
        db_table = 'profi_telegram_users'
        ordering = ['-date_join']
        verbose_name = _('Service user')
        verbose_name_plural = _('Service users')

    def __str__(self):

        if self.fio:
            return self.fio

        if self.telegram_username:
            return '@%s' % self.telegram_username

        if self.telegram_id:
            return 'Tg id %s' % self.telegram_id

        return 'User id %s' % self.id


class String(CacheModel, models.Model):
    """
    Текстовые сообщения и кнопки. Любые текстовые элементы бота
    """

    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('System name'), max_length=100, unique=True)
    category = models.CharField(_('Category'), max_length=255)
    value = models.TextField(_('Value'), max_length=1000, help_text=_('Formatting telegram message'))

    object = models.Manager()

    class Meta:
        db_table = 'profi_telegram_strings'
        ordering = ['category', 'name']
        verbose_name = _('Telegram message/button')
        verbose_name_plural = _('Telegram messages/buttons')

    def __str__(self):
        return '%s' % self.name

    @staticmethod
    def get_string(name):

        try:
            return String.cache.get(slug=name).value
        except String.DoesNotExist:
            return ''

    def print_value(self):
        s = self.value[:SHORT_VALUE_LENGTH-3]
        if len(self.value) > SHORT_VALUE_LENGTH:
            s += '...'
        return s
    print_value.short_description = _('Value')


class Menu(CacheModel, OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    value = models.TextField(_('Value'), help_text=_('Formatting telegram message'))

    object = models.Manager()

    class Meta:
        db_table = 'profi_telegram_menu'
        ordering = ['order']
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu')

    def __str__(self):
        return '%s' % self.name


class Report(PublicModel, models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    description = models.CharField(_('Description'), null=True, blank=True, max_length=200)
    file = models.FileField(_('File'), upload_to='profi/reports/%Y/%m/%d/')

    date_upload = models.DateTimeField(_('Date upload'), auto_now_add=True)

    class Meta:
        db_table = 'profi_reports'
        ordering = ['-date_upload']
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')

    def __str__(self):
        return '%s - %s' % (self.user, self.file)


class Task(OrderModel, PublicModel, models.Model):

    types = (
        ('good', _('Good job')),
    )

    name = models.CharField(_('Name'), max_length=1000)
    description = models.TextField(_('Description'), blank=True, null=True)
    price = models.FloatField(_('Price'), default=0, help_text=_('For a unit of work or goods'))

    is_offered = models.BooleanField(_('Is offered user'), default=False)
    author = models.ForeignKey(User, related_name='task_author', verbose_name=_('Author'), on_delete=models.SET_NULL,
                               blank=True, null=True)
    date_offered = models.DateTimeField(_('Date offered'), blank=True, null=True)
    type = models.CharField(_('Type'), default='good', choices=types, max_length=10)

    class Meta:
        db_table = 'profi_telegram_tasks'
        ordering = ['order']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):

        return self.name


class Order(models.Model):

    statuses = (
        ('new', _('New order')),
        ('checked', _('Checked')),
        ('invoice', _('Invoice')),
        ('wait', _('Wait working')),
        ('finished', _('Finished')),
    )

    user = models.ForeignKey(User, related_name='order_user', verbose_name=_('User'), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='order_task', verbose_name=_('Task'), on_delete=models.CASCADE)

    date_start = models.DateField(_('Date start'), null=True, blank=True)
    date_end = models.DateField(_('Date end'), null=True, blank=True)

    status = models.CharField(_('Status'), default='new', choices=statuses, max_length=20)

    clients = models.ManyToManyField(Client, related_name='order_clients', verbose_name=_('Clients'), blank=True)
    stores = models.ManyToManyField(Store, related_name='order_stores', verbose_name=_('Stores'), blank=True)
    regions = models.ManyToManyField(Region, related_name='order_regions', verbose_name=_('Regions'), blank=True)

    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    date_finish = models.DateTimeField(_('Date finish'), null=True, blank=True)

    is_not_moderate = models.BooleanField(_('Is not moderate'), default=False)
    not_moderate_description = models.TextField(_('Description'), null=True, blank=True)

    is_moderate = models.BooleanField(_('Is moderate'), default=False)
    moderate_description = models.TextField(_('Comment'), null=True, blank=True)

    is_invoice = models.BooleanField(_('Is invoice'), default=False)
    invoice_description = models.TextField(_('Comment'), null=True, blank=True)
    invoice_file = models.FileField(_('File'), upload_to='profi/invoices/', null=True, blank=True)

    is_finished = models.BooleanField(_('Is finished'), default=False)
    finished_description = models.TextField(_('Comment'), null=True, blank=True)

    per_week = models.IntegerField(_('How many times a week'), default=0, blank=True, choices=per_weeks)
    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')
    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)

    class Meta:
        db_table = 'profi_orders'
        ordering = ['-date_create']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return '%s %s' % (self.user, self.task)
