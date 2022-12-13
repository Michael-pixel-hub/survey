from django.db import models
from django.utils.translation import ugettext_lazy as _


class SolarStaffAccount(models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    salt = models.CharField(_('Salt value'), max_length=200)
    client_id = models.CharField(_('Client id'), max_length=200)

    class Meta:
        db_table = 'solar_staff_accounts'
        ordering = ['name']
        verbose_name = _('Solar staff account')
        verbose_name_plural = _('Solar staff accounts')

    def __str__(self):
        return self.name
