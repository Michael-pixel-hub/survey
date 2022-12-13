from application.survey.models import (
    TasksExecutionBase, Task, TasksExecutionImageBase, TasksExecutionAssortmentBeforeBase, Good,
    TasksExecutionAssortmentBase, TasksExecutionQuestionnaireBase
)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ArchiveTasksExecutionBase(TasksExecutionBase):

    date_start = models.DateTimeField(_('Date start'))
    task = models.ForeignKey(Task, related_name='%(app_label)s_%(class)s_task', verbose_name=_('Task'),
                             on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True


class ArchiveTasksExecution(ArchiveTasksExecutionBase):

    class Meta:
        managed = False
        db_table = 'archive_tasks_executions'
        ordering = ['-date_start']
        verbose_name = _('Task execution [archive]')
        verbose_name_plural = _('Tasks execution [archive]')


class ArchiveTasksExecutionImage(TasksExecutionImageBase):

    task = models.ForeignKey(ArchiveTasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    date_start = models.DateTimeField(_('Date start'))

    class Meta:
        managed = False
        db_table = 'archive_tasks_executions_images'


class ArchiveTasksExecutionAssortmentBefore(TasksExecutionAssortmentBeforeBase):

    task = models.ForeignKey(ArchiveTasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    date_start = models.DateTimeField(_('Date start'))

    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_good', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'archive_tasks_executions_assortment_before'


class ArchiveTasksExecutionAssortment(TasksExecutionAssortmentBase):

    task = models.ForeignKey(ArchiveTasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    date_start = models.DateTimeField(_('Date start'))

    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_good', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'archive_tasks_executions_assortment'


class ArchiveTasksExecutionQuestionnaire(TasksExecutionQuestionnaireBase):

    task = models.ForeignKey(ArchiveTasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    date_start = models.DateTimeField(_('Date start'))

    class Meta:
        managed = False
        db_table = 'archive_tasks_executions_questionnairess'
