from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SupervisorConfig(AppConfig):
    name = 'application.supervisor'
    verbose_name = 'Супервайзер'
    label = 'supervisor'

    def ready(self):
        super(SupervisorConfig, self).ready()

        # from application.survey.tasks import stores_tasks_refresh
        # print(stores_tasks_refresh())

        # from application.supervisor.tasks import supervisor_make_users_schedules
        # print(supervisor_make_users_schedules())

        # from application.survey.tasks import delete_account_notifications
        # print(delete_account_notifications())

        #from application.survey.models import TasksExecution
        #te = TasksExecution.objects.get(id=590676)
        #print(te.inspector_link_html())

        # from application.survey.tasks import request_process
        # print(request_process())
