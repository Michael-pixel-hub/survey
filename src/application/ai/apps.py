from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AIConfig(AppConfig):
    name = 'application.ai'
    verbose_name = _('Shop Survey AI')
    label = 'ai'

    def ready(self):
        super().ready()

        # from application.ai.tasks import ai_problem
        # print(ai_problem())
