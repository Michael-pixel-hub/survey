from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InspectorConfig(AppConfig):
    name = 'application.inspector'
    verbose_name = _('Inspector')
    label = 'inspector'

    def ready(self):
        super(InspectorConfig, self).ready()

        #from application.survey.tasks import auto_status
        #print(auto_status())

        #from .tasks import inspector_alert_constructor
        #print(inspector_alert_constructor())
