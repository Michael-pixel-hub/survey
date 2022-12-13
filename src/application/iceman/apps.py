from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IcemanConfig(AppConfig):
    name = 'application.iceman'
    verbose_name = _('Iceman')
    label = 'iceman'

    def ready(self):
        super().ready()

        # from application.iceman.tasks import iceman_fill_stores_tasks
        # print(iceman_fill_stores_tasks())
