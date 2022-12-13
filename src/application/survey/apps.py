from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SurveyConfig(AppConfig):
    name = 'application.survey'
    verbose_name = _('Chistaya liniya')
    label = 'survey'

    def ready(self):
        super(SurveyConfig, self).ready()

        # from application.survey.tasks import auto_status
        # print(auto_status())

        # from application.survey.tasks import delete_account_notifications
        # print(delete_account_notifications())

        #from application.survey.models import TasksExecution
        #te = TasksExecution.objects.get(id=590676)
        #print(te.inspector_link_html())

        # from application.survey.tasks import request_process
        # print(request_process())
