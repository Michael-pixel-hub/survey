from django.db import models
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel
from sort_model.models import OrderModel

actions = (
    ('show_text', _('Show text')),
    ('debt', _('Receivables')),
)


class Department(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200)
    sys_name = models.CharField(_('System name'), max_length=100, unique=True)

    class Meta:
        db_table = 'loyalty_departments'
        ordering = ['name']
        verbose_name = _('Loyalty department')
        verbose_name_plural = _('Loyalty departments')

    def __str__(self):
        return '%s' % self.name


class DepartmentMenuItem(OrderModel, PublicModel, models.Model):

    department = models.ForeignKey(Department, verbose_name=_('Loyalty department'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100)
    value = models.TextField(_('Description'), help_text=_('Formatting telegram message'), blank=True, default='')
    action = models.TextField(_('Action'), max_length=20, default='show_text', choices=actions)
    file = models.FileField(_('File'), upload_to='loyalty/menus/', null=True, blank=True)
    url = models.CharField(_('Url'), null=True, blank=True, max_length=200)

    class Meta:
        db_table = 'loyalty_departments_menu'
        ordering = ['department__name', 'order']
        verbose_name = _('Loyalty department menu item')
        verbose_name_plural = _('Loyalty departments menu items')
        unique_together = (('department', 'name'),)

    def __str__(self):
        return '%s' % self.name


class Program(OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    sys_name = models.CharField(_('System name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    file = models.FileField(_('File'), upload_to='loyalty/programs/', null=True, blank=True)
    url = models.CharField(_('Url'), null=True, blank=True, max_length=200)

    class Meta:
        db_table = 'loyalty_programs'
        ordering = ['order']
        verbose_name = _('Loyalty program')
        verbose_name_plural = _('Loyalty programs')

    def __str__(self):
        return '%s' % self.name


class ProgramPeriod(models.Model):

    program = models.ForeignKey(Program, verbose_name=_('Loyalty program'), on_delete=models.CASCADE)
    date_start = models.DateField(_('Start date'))
    date_end = models.DateField(_('End date'))
    current = models.BooleanField(_('Current period'), default=False)

    class Meta:
        db_table = 'loyalty_programs_periods'
        ordering = ['date_start', 'date_end']
        verbose_name = _('Loyalty program period')
        verbose_name_plural = _('Loyalty program periods')

    def __str__(self):
        return '%s - %s' % (self.date_start, self.date_end)


class Store(models.Model):

    name = models.CharField(_('Name'), max_length=255)
    contact = models.CharField(_('Contact face'), max_length=255, blank=True, default='')
    phone = models.CharField(_('Phone'), max_length=30, blank=True, default='')
    address = models.CharField(_('Address'), max_length=1000, blank=True, default='')
    inn = models.CharField(_('Inn'), max_length=12, blank=True, default='')
    city = models.CharField(_('City'), max_length=255, blank=True, default='')
    agent = models.CharField(_('Sales Representative'), max_length=1000, blank=True, default='')

    loyalty_department = models.ForeignKey(Department, related_name='story_department', verbose_name=_('Department'),
                                           on_delete=models.SET_NULL, blank=True, null=True)
    loyalty_program = models.ForeignKey(Program, related_name='story_program', verbose_name=_('Loyalty program'),
                                        on_delete=models.SET_NULL, blank=True, null=True)
    loyalty_1c_code = models.CharField(_('1c code'), max_length=100, unique=True)
    loyalty_1c_user = models.CharField(_('1c code user'), max_length=200, blank=True, null=True)

    loyalty_plan = models.FloatField(_('Loyalty plan'), default=0)
    loyalty_fact = models.FloatField(_('Loyalty fact'), default=0)
    loyalty_cashback = models.FloatField(_('Loyalty cashback'), default=0)
    loyalty_sumcashback = models.FloatField(_('Loyalty sumcashback'), default=0)
    loyalty_debt = models.FloatField(_('Loyalty debt'), default=0)
    loyalty_overdue_debt = models.FloatField(_('Loyalty overdue_debt'), default=0)

    price_type = models.CharField(_('Price type'), max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'loyalty_stores'
        ordering = ['loyalty_1c_code']
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return '%s' % self.name
