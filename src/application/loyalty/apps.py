from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LoyaltyConfig(AppConfig):
    name = 'application.loyalty'
    verbose_name = _('Loyalty bot')
    label = 'loyalty'

    def ready(self):
        super(LoyaltyConfig, self).ready()

        # from application.survey.tasks import request_process
        # print(request_process())
