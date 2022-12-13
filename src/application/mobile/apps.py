from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MobileConfig(AppConfig):
    name = 'application.mobile'
    verbose_name = _('Mobile app')
    label = 'mobile'

    def ready(self):
        super(MobileConfig, self).ready()

        # from application.mobile.tasks import mobile_push
        # print(mobile_push())

        #from .tasks import inspector_alert_constructor
        #print(inspector_alert_constructor())
