from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AgentConfig(AppConfig):
    name = 'application.agent'
    verbose_name = _('Agent')
    label = 'agent'

    def ready(self):
        super(AgentConfig, self).ready()
        import application.agent.signals

        #from application.agent.tasks import calc_cashback
        #print(calc_cashback())
