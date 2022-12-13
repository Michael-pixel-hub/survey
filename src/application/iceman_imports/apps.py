from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IcemanImportsConfig(AppConfig):
    name = 'application.iceman_imports'
    verbose_name = _('Iceman')
    label = 'iceman_imports'

    def ready(self):
        super().ready()
