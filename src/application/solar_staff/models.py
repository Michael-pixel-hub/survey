from django.db import models
from django.utils.translation import ugettext_lazy as _

from application.agent.models import Order
from application.survey.models import User, Task, TasksExecution
from application.solar_staff_accounts.models import SolarStaffAccount


class SolarStaffPayments(models.Model):

    codes = (
        (100, _('Error')),
        (1, _('Waiting for confirm')),
        (2, _('Success')),
        (3, _('Declined')),
        (4, _('Refunded')),
        (5, _('Partially completed')),
    )

    types = (
        (1, _('Task execution')),
        (2, _('Order cashback')),
        (3, _('Custom payment')),
    )

    date_payed = models.DateTimeField(_('Date payed'), auto_now_add=True)

    te = models.ForeignKey(TasksExecution, related_name='solar_task', verbose_name=_('Task execution'),
                           on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, related_name='solar_order', verbose_name=_('Order'), on_delete=models.CASCADE,
                              blank=True, null=True)

    email = models.CharField(_('E-mail'), blank=True, null=True, max_length=100)
    first_name = models.CharField(_('Name'), blank=True, null=True, max_length=100)
    last_name = models.CharField(_('Surname'), blank=True, null=True, max_length=100)

    server_code = models.IntegerField(_('Status'), default=100, choices=codes)
    server_error = models.TextField(_('Error text'), blank=True, null=True)
    server_response = models.TextField(_('Server response'), blank=True, null=True, help_text=_('For debugging'))

    type = models.IntegerField(_('Type'), default=1, choices=types)

    sum = models.FloatField(_('Sum'), blank=True, null=True)

    account = models.ForeignKey(SolarStaffAccount, related_name='solar_account', verbose_name=_('Account'),
                                on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'solar_staff_payments'
        ordering = ['-date_payed']
        verbose_name = _('Payment history')
        verbose_name_plural = _('Payments history')
        indexes = [
            models.Index(fields=['server_code']),
            models.Index(fields=['server_error']),
            models.Index(fields=['server_response']),
            models.Index(fields=['email']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
        ]

    def __str__(self):
        return 'Платеж %s для %s' % (self.date_payed, self.email)


class Payment(models.Model):

    statuses = (
        (1, _('New')),
        (2, _('Pay in Solar')),
        (3, _('Payed')),
        (4, _('Error payment')),
    )

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    sum = models.FloatField(_('Payment sum'), default=0)
    status = models.IntegerField(_('Status'), default=1, choices=statuses)
    comment = models.TextField(_('Comment'), max_length=1000)

    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    date_payment = models.DateTimeField(_('Date payment'), null=True, blank=True)

    ss_account = models.ForeignKey(SolarStaffAccount, related_name='payment_ss_account',
                                   verbose_name=_('Solar staff account'),
                                   on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'chl_payments'
        ordering = ['-date_create']
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return 'Платеж %s для %s' % (self.comment, self.user)
