from application.survey.models import User, TasksExecution

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserSchedule(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_schedule_user')
    date = models.DateField(_('Date'))
    route = models.CharField(_('Route name'), max_length=255, default='')

    class Meta:
        db_table = 'supervisors_users_schedules'
        ordering = ['date', 'route', 'user__surname', 'user__name']
        verbose_name = 'Расписание пользователя'
        verbose_name_plural = 'Расписания пользователей'
        unique_together = (('user', 'date'), )

    def __str__(self):
        return f'Расписание пользователя "{self.user.email}" на дату "{self.date}"'


class UserScheduleTaskExecution(models.Model):

    schedule = models.ForeignKey(UserSchedule, verbose_name='Расписание пользователя', on_delete=models.CASCADE)

    te = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.SET_NULL, null=True,
                           blank=True)

    task_id = models.IntegerField(_('Task id'))
    store_id = models.IntegerField(_('Store id'))

    store_code = models.CharField(_('Store code'), max_length=100)
    store_client_name = models.CharField(_('Store client name'), max_length=100)
    store_category_name = models.CharField(_('Store category name'), max_length=100)
    store_address = models.TextField(_('Store address'), max_length=500)

    task_name = models.CharField(_('Task name'), max_length=100)

    class Meta:
        db_table = 'supervisors_users_schedules_te'
        ordering = ['schedule__id', 'id']
        verbose_name = 'Расписание пользователя'
        verbose_name_plural = 'Расписания пользователей'
        unique_together = (('task_id', 'store_id', 'schedule'),)

    def __str__(self):
        return f'Посещение пользователем ' \
               f'"{self.schedule.user.email}" точки "{self.store_code}" с задачей "{self.task_name}"'
