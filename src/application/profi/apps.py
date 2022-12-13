from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProfiConfig(AppConfig):
    name = 'application.profi'
    verbose_name = _('Profi bot')
    label = 'profi'

    def ready(self):
        super(ProfiConfig, self).ready()
