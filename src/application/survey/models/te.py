import datetime
import hashlib
import json
import uuid

from django.db import models, transaction
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from public_model.models import PublicModel
from application.users.models import User as DjangoUser
from application.inspector.models import InspectorGood
from application.iceman.models import Store as IcemanStore

from ..utils import get_coordinates, send_user_status_change
from .all import Task, Store, Good,  User, TaskStep, TaskQuestionnaire, StoreTask, OutReason


class TasksExecutionBase(models.Model):

    statuses = (
        (1, _('Started')),
        (2, _('Finished')),
        (3, _('Checked')),
        (6, _('Pay in Solar')),
        (4, _('Payed')),
        (5, _('Denied')),
        (7, _('Not payed')),
        (8, _('Temp denied')),
    )

    inspector_statuses = (
        ('undefined', _('Undefined')),
        ('wait', _('Waiting for inspector')),
        ('upload_wait', _('Upload wait')),
        ('upload_error', _('Upload error')),
        ('parse_error', _('Parse error')),
        ('report_process', _('Report process')),
        ('report_error', _('Report error')),
        ('report_wait', _('Report waiting')),
        ('error', _('Error')),
        ('success', _('Success parsing')),
        ('ai', _('Shop survey AI')),
    )

    steps = (
        ('before', _('Photo before')),
        ('after', _('Photo after')),
        ('check', _('Photo check')),
        ('uploaded', _('All photo uploaded')),
    )
    check_types = (
        ('not_verified', _('Not verified')),
        ('true', _('Correct check')),
        ('false', _('Incorrect check')),
        ('not_need', 'Не нужно'),
    )
    checks_types = (
        ('not_checked', 'Ожидает проверки'),
        ('checked', 'Проверен'),
        ('not_need', 'Не нужно'),
    )
    telegram_channel_types = (
        (0, _('Not need')),
        (1, _('Wait')),
        (2, _('Sent')),
    )

    sources = (
        ('undefined', _('Unknown')),
        ('telegram', _('Telegram')),
        ('android', _('Android')),
        ('iphone', _('iPhone')),
        ('admin', 'Админка'),
    )

    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_user', verbose_name=_('User'),
                             on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='%(app_label)s_%(class)s_task', verbose_name=_('Task'),
                             on_delete=models.CASCADE)
    money = models.FloatField(_('Sum'), default=0)
    money_source = models.FloatField(_('Sum source'), default=0)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)
    date_end_user = models.DateTimeField(_('Date end user'), null=True, blank=True)
    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    store = models.ForeignKey(Store, related_name='%(app_label)s_%(class)s_store', verbose_name=_('Store'),
                              on_delete=models.SET_NULL, null=True, blank=True)
    store_iceman = models.ForeignKey(IcemanStore, related_name='%(app_label)s_%(class)s_store_iceman',
                                     verbose_name=_('Store'), on_delete=models.SET_NULL, null=True, blank=True)

    image = models.FileField(_('Confirmation image'), upload_to='tasks/exec/%Y/%m/%d/', null=True, blank=True)
    comments = models.TextField(_('Comments'), blank=True, default='', help_text=_('What the user writes'))
    comments_status = models.TextField(_('Status comments'), blank=True, default='',
                                       help_text=_('What comes to the user when the status changes'), null=True)
    comments_internal = models.TextField(_('Internal comments'), blank=True, default='', null=True,
                                         help_text=_('Remains in the system and is visible only to administrators.'))

    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    distance = models.FloatField(_('Distance to store'), null=True, blank=True, help_text=_('Meters'))

    step = models.CharField(_('Step'), default='before', choices=steps, max_length=10)
    check_type = models.CharField(_('Check'), default='not_need', choices=check_types, max_length=12)
    check = models.CharField('Проверка', default='not_need', choices=checks_types, max_length=12)
    set_check_verified = models.BooleanField(_('Set check verified'), blank=True, default=False)
    set_check_not_verified = models.BooleanField(_('Set check not verified'), blank=True, default=False)
    is_auditor = models.BooleanField(_('Checked by auditor'), blank=True, default=False)
    check_user = models.ForeignKey(DjangoUser, related_name='%(app_label)s_%(class)s_check_user',
                                   verbose_name='Аудитор причин/чека', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    inspector_upload_images_text = models.TextField(_('Upload images message'), blank=True, default='')
    inspector_error = models.TextField(_('Error text'), blank=True, default='', null=True)
    inspector_recognize_text = models.TextField(_('Recognize message'), blank=True, default='', null=True)
    inspector_report_text = models.TextField(_('Report'), blank=True, default='', null=True)
    inspector_positions_text = models.TextField(_('Positions text'), blank=True, default='', null=True)
    inspector_status = models.CharField(_('Inspector status'), default='wait', choices=inspector_statuses,
                                        max_length=20)
    inspector_report_id = models.IntegerField(_('Report id'), blank=True, null=True)

    inspector_report_id_before = models.IntegerField(_('Report id before'), blank=True, null=True)
    inspector_status_before = models.CharField(_('Inspector status before'), default='wait', choices=inspector_statuses,
                                               max_length=20)

    inspector_is_alert = models.BooleanField(_('Inspector alert'), blank=True, default=False)
    inspector_re_work = models.BooleanField(_('Inspector re work'), blank=True, default=False)
    inspector_is_work = models.BooleanField(_('Inspector is work'), blank=True, default=False)

    telegram_channel_status = models.IntegerField(_('Telegram channel status'), default=0,
                                                  choices=telegram_channel_types)

    source = models.CharField(_('Source'), default='undefined', choices=sources, max_length=20)
    source_name = models.CharField('Название устройства', max_length=255, null=True, blank=True)
    source_os = models.CharField('Операционная система', max_length=255, null=True, blank=True)
    source_os_version = models.CharField('Версия ОС', max_length=255, null=True, blank=True)
    source_version = models.CharField('Версия приложения', max_length=255, null=True, blank=True)

    constructor_step = models.ForeignKey(
        TaskStep, related_name='%(app_label)s_%(class)s_constructor_step', verbose_name=_('Task step'),
        on_delete=models.SET_NULL, null=True, blank=True
    )

    application = models.CharField('Проект', default='shop_survey', choices=settings.APPLICATIONS, max_length=20)

    is_fake_gps = models.BooleanField('Подмена GPS', blank=True, null=True)
    is_api_direct = models.BooleanField('Напрямую через API', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        store = self.store.code if self.store else '-'
        if store == '-':
            store = self.store_iceman.code if self.store_iceman else '-'
        return '"%s" [%s] в магазине: %s' % (
            self.task if self.task else '-',
            self.user.email if self.user else '-',
            store
        )

    @cached_property
    def user_object(self):
        return self.user
    user_object.short_description = _('User')

    @cached_property
    def task_object(self):
        return self.task
    task_object.short_description = _('Task')

    @cached_property
    def store_short(self):
        if self.store_iceman:
            s = str(self.store_iceman)
            if len(s) > 100:
                s = s[:100] + '...'
        else:
            s = str(self.store)
            if len(s) > 100:
                s = s[:100] + '...'
        return s
    store_short.short_description = _('Store')

    @cached_property
    def user_name(self):
        return self.user.name
    user_name.short_description = _('User name')

    @cached_property
    def user_rank(self):
        try:
            return self.user.rank.name
        except:
            return '-'
    user_rank.short_description = _('Rank')

    @cached_property
    def user_status_legal(self):
        try:
            return self.user.get_status_legal_display()
        except:
            return '-'
    user_status_legal.short_description = _('Legal status')

    @cached_property
    def user_surname(self):
        return self.user.surname
    user_surname.short_description = _('Surname')

    def inspector_link(self):
        try:
            s = self.inspector_recognize_text.replace('\'', '"')
            data = json.loads(s)
            return 'https://chl.inspector-cloud.ru/portal/visit/%s/scene/%s?tab=1' % (data['visit'], data['id'])
        except:
            pass

    inspector_link.short_description = _('Inspector link')

    def inspector_link_html(self):
        s = self.inspector_link()
        if s:
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (s, s))
        else:
            return '-'
    inspector_link_html.short_description = _('Inspector link')


class TasksExecution(TasksExecutionBase):

    __original_status = None

    audit_user = models.ForeignKey(DjangoUser, related_name='%(app_label)s_%(class)s_audit_user',
                                   verbose_name='Аудитор задачи', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'chl_tasks_executions'
        ordering = ['-date_start']
        verbose_name = _('Task execution')
        verbose_name_plural = _('Tasks execution')
        indexes = [
            models.Index(fields=['comments']),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        self.money = round(self.money, 2)
        self.money_source = round(self.money_source, 2)

        if self.set_check_not_verified:
            self.check_type = 'false'
            self.set_check_not_verified = False

        if self.set_check_verified:
            self.check_type = 'true'
            self.set_check_verified = False

        with open('/var/log/shop-survey/statuses.log', 'a') as f:
            f.write(
                f'Change status from {self.__original_status} to {self.status}. Date: {datetime.datetime.now()}. Id: {self.id}\r\n')
            f.close()

        if self.status != self.__original_status and self.status == 6:

            pass

            # Платеж
            #from application.survey.solar_staff.tasks import solar_staff_pay
            #solar_staff_pay.apply_async((self.id, ), countdown=60)

        if self.id is not None and self.__original_status is not None \
                and self.status != self.__original_status and self.status in [3, 4, 5]:

            # Отправка сообщения
            old_status = 'Нет'
            for i in self.statuses:
                if i[0] == self.__original_status:
                    old_status = i[1]
            send_user_status_change(self, old_status)

        # Отказ снимаем лок
        if self.status != self.__original_status and self.status == 5:
            try:
                st_obj = StoreTask.objects.get(task=self.task, store=self.store)
                try:
                    sta = StoreTaskAvail.objects.get(store_task_id=st_obj.id)
                    sta.update_time = datetime.datetime.now()
                    sta.lock_user_id = None
                    sta.deleted = False
                    sta.save()
                except StoreTaskAvail.DoesNotExist:
                    pass
            except StoreTask.DoesNotExist:
                pass

        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status


class TasksExecutionCheck(TasksExecution):
    class Meta:
        proxy = True
        verbose_name = _('Task execution check')
        verbose_name_plural = _('Tasks execution checks')
        ordering = ['date_start']


class TasksExecutionCheckInspector(TasksExecution):
    class Meta:
        proxy = True
        verbose_name = _('Task execution')
        verbose_name_plural = 'Проверка причин ООS'
        ordering = ['date_start']


class TasksExecutionStep(models.Model):

    types = (
        ('photos', _('Photos')),
        ('comment', _('Comment')),
        ('questionnaire', _('Questionnaire')),
    )

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    date_start = models.DateTimeField('Дата начала', blank=True, null=True)
    date_end = models.DateTimeField('Дата завершения', blank=True, null=True)
    name = models.CharField(_('Name'), max_length=200)
    step_type = models.CharField(_('Step type'), max_length=20, default='photos', choices=types)
    is_skip = models.BooleanField('Шаг пропущен', default=False)

    class Meta:
        db_table = 'chl_tasks_executions_steps'
        ordering = ['-task__date_start', 'date_start', 'id']
        verbose_name = 'Шаг выполнения задачи'
        verbose_name_plural = 'Шаги выполнения задачи'

    def __str__(self):
        return '%s' % self.name


class TasksExecutionInspector(models.Model):

    inspector_statuses = (
        ('undefined', _('Undefined')),
        ('wait', _('Waiting for inspector')),
        ('upload_wait', _('Upload wait')),
        ('upload_error', _('Upload error')),
        ('parse_error', _('Parse error')),
        ('report_process', _('Report process')),
        ('report_error', _('Report error')),
        ('report_wait', _('Report waiting')),
        ('error', _('Error')),
        ('success', _('Success parsing')),
    )

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    constructor_step_name = models.CharField(_('Step name'), max_length=200, default='', blank=True)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)

    inspector_upload_images_text = models.TextField(_('Upload images message'), blank=True, default='')
    inspector_error = models.TextField(_('Error text'), blank=True, default='', null=True)
    inspector_recognize_text = models.TextField(_('Recognize message'), blank=True, default='', null=True)
    inspector_report_text = models.TextField(_('Report'), blank=True, default='', null=True)
    inspector_positions_text = models.TextField(_('Positions text'), blank=True, default='', null=True)
    inspector_status = models.CharField(_('Inspector status'), default='wait', choices=inspector_statuses,
                                        max_length=20)
    inspector_report_id = models.IntegerField(_('Report id'), blank=True, null=True)

    inspector_is_alert = models.BooleanField(_('Inspector alert'), blank=True, default=False)

    class Meta:
        db_table = 'chl_tasks_executions_inspector'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Task execution inspector')
        verbose_name_plural = _('Tasks execution inspector')

    def save_to_te(self):
        if self.task.source == 'telegram':
            self.task.inspector_upload_images_text = self.inspector_upload_images_text
            self.task.inspector_error = self.inspector_error
            self.task.inspector_recognize_text = self.inspector_recognize_text
            self.task.inspector_report_text = self.inspector_report_text
            self.task.inspector_positions_text = self.inspector_positions_text
            self.task.inspector_status = self.inspector_status
            self.task.inspector_report_id = self.inspector_report_id
            self.task.save(update_fields=['inspector_upload_images_text', 'inspector_error',
                                          'inspector_recognize_text', 'inspector_report_text', 'inspector_status',
                                          'inspector_status', 'inspector_report_id'])

    def inspector_link(self):
        try:
            s = self.inspector_recognize_text.replace('\'', '"')
            data = json.loads(s)
            return 'https://chl.inspector-cloud.ru/portal/visit/%s/scene/%s?tab=1' % (data['visit'], data['id'])
        except:
            pass

    inspector_link.short_description = _('Inspector link')

    def inspector_link_html(self):
        s = self.inspector_link()
        if s:
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (s, s))
        else:
            return '-'
    inspector_link_html.short_description = _('Inspector link')


class TasksExecutionQuestionnaireBase(models.Model):

    name = models.CharField(_('Name'), max_length=200)
    question = models.CharField(_('Question text'), max_length=1000)
    answer = models.CharField(_('Answer'), max_length=1000, blank=True, default='')
    constructor_step_name = models.CharField(_('Step name'), max_length=200, default='', blank=True)

    class Meta:
        abstract = True
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Task questionnaire answer')
        verbose_name_plural = _('Task questionnaire answers')
        unique_together = (('name', 'task', 'constructor_step_name'), )

    def __str__(self):
        return '%s' % self.name


class TasksExecutionQuestionnaire(TasksExecutionQuestionnaireBase):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')

    class Meta:
        db_table = 'chl_tasks_executions_questionnaires'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Task questionnaire answer')
        verbose_name_plural = _('Task questionnaire answers')
        unique_together = (('name', 'task', 'constructor_step_name'), )


class TasksExecutionImageBase(models.Model):

    image_types = (
        ('undefined', _('Undefined')),
        ('enter', _('Enter photo')),
        ('before', _('Photo before work')),
        ('after', _('Photo after work')),
        ('check', _('Cass check')),
    )

    image = models.FileField(_('Image'), upload_to='tasks/exec/%Y/%m/%d/', null=True, blank=True,
                             db_index=True)
    status = models.CharField(_('Unique status'), max_length=1000, default=str(_('Image analysis in progress...')),
                              db_index=True)
    md5 = models.CharField('Md5 sum', max_length=32, blank=True, null=True, db_index=True)

    type = models.CharField(_('Image type'), max_length=10, default='undefined', choices=image_types)

    constructor_step_name = models.CharField(_('Step name'), max_length=200, default='', blank=True)
    constructor_check = models.BooleanField(_('Check'), blank=True, default=False)

    telegram_id = models.CharField(_('Telegram id'), max_length=200, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Confirmation image')
        verbose_name_plural = _('Confirmation images')

    def __str__(self):
        return '%s' % self.image.path


class TasksExecutionImage(TasksExecutionImageBase):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')

    class Meta:
        db_table = 'chl_tasks_executions_images'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Confirmation image')
        verbose_name_plural = _('Confirmation images')

    def save(self, *args, **kwargs):
        try:
            md5sum = hashlib.md5(open(self.image.path, 'rb').read()).hexdigest()
            self.md5 = md5sum
        except:
            pass
        super(TasksExecutionImage, self).save(*args, **kwargs)


class TasksExecutionAssortmentBase(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_good')
    avail = models.FloatField(_('Avail'))
    constructor_step_name = models.CharField(_('Step name'), max_length=200, default='', blank=True)

    class Meta:
        abstract = True
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment')
        verbose_name_plural = _('Avail assortments')

    def __str__(self):
        return '%s' % self.good


class TasksExecutionAssortment(TasksExecutionAssortmentBase):

    class Meta:
        db_table = 'chl_tasks_executions_assortment'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment')
        verbose_name_plural = _('Avail assortments')


class TasksExecutionAssortmentAll(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='tea_a_task')
    good = models.ForeignKey(InspectorGood, verbose_name=_('Good'), on_delete=models.CASCADE, related_name='tea_a_good')
    avail = models.FloatField(_('Avail'))

    class Meta:
        db_table = 'chl_tasks_executions_assortment_all'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment all')
        verbose_name_plural = _('Avail assortments all')

    def __str__(self):
        return '%s' % self.good


class TasksExecutionAssortmentBeforeBase(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_good')
    avail = models.FloatField(_('Avail'))

    class Meta:
        abstract = True
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment before')
        verbose_name_plural = _('Avail assortments before')

    def __str__(self):
        return '%s' % self.good


class TasksExecutionAssortmentBefore(TasksExecutionAssortmentBeforeBase):

    class Meta:
        db_table = 'chl_tasks_executions_assortment_before'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment before')
        verbose_name_plural = _('Avail assortments before')


class TasksExecutionOutReasonBase(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_task')
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_good')                             
    out_reason = models.ForeignKey(OutReason, verbose_name='Причина отсутствия', on_delete=models.CASCADE,
                                   related_name='%(app_label)s_%(class)s_task')
    image = models.FileField(_('Image'), upload_to='tasks/out_reasons/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-task__date_start', 'id']
        verbose_name = 'Причина отсутствия товара'
        verbose_name_plural = 'Причины отсутствия товаров'

    def __str__(self):
        return '%s - %s' % (self.good, self.out_reason)


class TasksExecutionOutReason(TasksExecutionOutReasonBase):

    class Meta:
        db_table = 'chl_tasks_executions_out_reasons'
        ordering = ['-task__date_start', 'id']
        verbose_name = 'Причина отсутствия товара'
        verbose_name_plural = 'Причины отсутствия товаров'


class Act(models.Model):

    check_types = (
        ('new', _('New act')),
        ('wait', _('Waiting for verify')),
        ('true', _('Correct check')),
        ('false', _('Incorrect check')),
    )

    number = models.CharField(_('Number'), max_length=100)
    id_1c = models.CharField(_('1c id'), max_length=255, unique=True, blank=True, null=True)
    date = models.DateTimeField(_('Date'))
    date_update = models.DateTimeField(_('Date update'), auto_now=True)

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL,
                             related_name='%(app_label)s_%(class)s_user', blank=True, null=True)
    user_fio = models.CharField(_('Fio'), max_length=255, blank=True, null=True)
    user_inn = models.CharField(_('INN'), max_length=20, blank=True, null=True)
    user_phone = models.CharField(_('Phone'), max_length=50, blank=True, null=True)
    user_email = models.CharField(_('E-mail'), max_length=255, blank=True, null=True)

    sum = models.FloatField(_('Sum'), blank=True, null=True)
    date_start = models.DateTimeField(_('Date start'), blank=True, null=True)
    date_end = models.DateTimeField(_('Date end'), blank=True, null=True)

    is_sent_telegram = models.BooleanField(_('Sent telegram'), default=False)

    check_type = models.CharField(_('Check'), default='new', choices=check_types, max_length=12)
    set_check_verified = models.BooleanField(_('Set check verified'), blank=True, default=False)
    set_check_not_verified = models.BooleanField(_('Set check not verified'), blank=True, default=False)
    check_user = models.ForeignKey(DjangoUser, related_name='%(app_label)s_%(class)s_check_user',
                                   verbose_name=_('Check user'), on_delete=models.SET_NULL, null=True, blank=True)

    url = models.CharField(_('Link'), null=True, blank=True, max_length=255)
    comment_manager = models.TextField(_('Manager comment'), blank=True, null=True)

    class Meta:
        db_table = 'chl_acts'
        ordering = ['-number']
        verbose_name = _('Act')
        verbose_name_plural = _('Acts')

    def __str__(self):
        return f'{self.number} - {self.date} - {self.user_fio}'

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.set_check_not_verified:
            self.check_type = 'false'
            self.set_check_not_verified = False
            self.is_sent_telegram = False

        if self.set_check_verified:
            self.check_type = 'true'
            self.set_check_verified = False
            self.is_sent_telegram = False

        super().save(force_insert, force_update, *args, **kwargs)


class ActCheck(Act):

    class Meta:
        proxy = True
        verbose_name = _('Check act taxpayers')
        verbose_name_plural = _('Check acts taxpayers')


class StoreTaskAvail(models.Model):

    store_task_id = models.IntegerField(_('Store task id'), unique=True)
    task_id = models.IntegerField(_('Task id'))

    store_id = models.IntegerField(_('Store id'))
    store_code = models.CharField(_('Store code'), max_length=100, blank=True)
    store_client_name = models.CharField(_('Store client name'), max_length=100)
    store_category_name = models.CharField(_('Store category name'), max_length=100, blank=True)
    store_region_name = models.CharField(_('Store region name'), max_length=100, blank=True)
    store_region_id = models.IntegerField(_('Store region id'), null=True, blank=True)
    store_address = models.TextField(_('Store address'), max_length=500, blank=True)
    store_longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    store_latitude = models.FloatField(_('Latitude'), null=True, blank=True)

    only_user_id = models.IntegerField(_('Only user id'), null=True, blank=True)
    lock_user_id = models.IntegerField(_('Lock user id'), null=True, blank=True)

    is_add_value = models.BooleanField(_('Is add value'), default=False, blank=True)
    add_value = models.FloatField(_('New value'), blank=True, null=True)

    is_delete = models.BooleanField(_('Is delete'), default=False)
    telegram_channel_id = models.CharField(_('Telegram channel id'), max_length=100, blank=True, null=True)

    update_time = models.DateTimeField(_('Update time'), blank=True, null=True)
    deleted = models.BooleanField(_('Is deleted'), default=False)

    position = models.IntegerField('Последовательность', blank=True, null=True)

    class Meta:
        db_table = 'chl_stores_tasks_avail'
        ordering = ['id']
        verbose_name = _('Store task avail')
        verbose_name_plural = _('Stores tasks avails')

    def __str__(self):
        return _('Store task avail # %s') % self.store_task_id


class Import(models.Model):

    statuses = (
        (1, _('In process')),
        (2, _('Finished')),
        (3, _('Canceled')),
        (4, _('Error')),
    )

    file_name = models.CharField(_('File name'), max_length=255)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)

    rows_count = models.IntegerField(_('Rows count'), null=True, blank=True)
    rows_process = models.IntegerField(_('Rows process'), blank=True, default=0)

    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    report_text = models.TextField(_('Report text'), null=True, blank=True)

    user = models.ForeignKey(DjangoUser, related_name='survey_import_user', verbose_name=_('User'),
                             on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(_('File'), upload_to='imports/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'chl_imports'
        ordering = ['-date_start']
        verbose_name = _('Data import')
        verbose_name_plural = _('Data imports')

    def __str__(self):
        return '%s' % self.date_start


class ImportTask(models.Model):

    statuses = (
        (1, _('In process')),
        (2, _('Finished')),
        (3, _('Canceled')),
        (4, _('Error')),
    )

    file_name = models.CharField(_('File name'), max_length=255)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)

    rows_count = models.IntegerField(_('Rows count'), null=True, blank=True)
    rows_process = models.IntegerField(_('Rows process'), blank=True, default=0)

    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    report_text = models.TextField(_('Report text'), null=True, blank=True)

    user = models.ForeignKey(DjangoUser, related_name='survey_import_tasks_user', verbose_name=_('User'),
                             on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(_('File'), upload_to='imports/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'chl_imports_tasks'
        ordering = ['-date_start']
        verbose_name = _('Task import')
        verbose_name_plural = _('Tasks imports')

    def __str__(self):
        return '%s' % self.date_start


class Penalty(models.Model):
    """
    Модель "Штраф"
    """
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_user', verbose_name=_('User'),
                             on_delete=models.CASCADE)
    amount = models.FloatField(_('Сумма штрафа'), default=0)
    repayment_amount = models.FloatField(_('Сумма погашения штрафа'), default=0)
    creator = models.ForeignKey(DjangoUser, related_name='%(app_label)s_%(class)s_creator',
                                verbose_name=_('Координатор'), on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        db_table = 'survey_penalty'
        ordering = ['user']
        verbose_name = 'Штраф сюрвеера'
        verbose_name_plural = 'Штрафы'

    def __str__(self):
        return f'{self.user} {self.amount}'
    
    @property
    def is_repaid(self):
        """
        Флаг полного погашения штрафа
        """
        if self.repayment_amount == self.amount:
            return True
        else:
            return False
    
    @receiver(post_save, sender=TasksExecution, dispatch_uid=str(uuid.uuid4()))
    def update_repayment_amount_by_save_te(sender, instance, **kwargs):
        """
        Метод обновления суммы погашения за счет задачи te по сигналу post_save при создании задачи
        и ее изменении
        """
        if instance.status == 3 and instance.money != 0:
            with transaction.atomic():
                user_penalties = Penalty.objects.filter(
                    user=instance.user,
                    date_create__lt=instance.date_start
                ).exclude(
                    repayment_amount=F('amount')
                ).all()
                if user_penalties:
                    penalty_list = []
                    penalty_repayment_list = []
                    i = 0
                    len_user_penalties = len(user_penalties)
                    penalty = user_penalties[i]
                    while (instance.money != 0 and
                           i < len_user_penalties and
                           not penalty.is_repaid):
                        penalty = user_penalties[i]
                        if (penalty.repayment_amount + instance.money) > penalty.amount:
                            repayment_sum = penalty.amount - penalty.repayment_amount
                            penalty.repayment_amount = penalty.amount
                        else:
                            penalty.repayment_amount = penalty.repayment_amount + instance.money
                            repayment_sum = instance.money
                        penalty.save()
                        PenaltyRepayment.objects.create(penalty=penalty, te=instance,
                                                        repayment_sum=round(repayment_sum, 1))
                        instance.money -= repayment_sum
                        instance.save()
                        i += 1
        elif instance.status == 5:
            PenaltyRepayment.objects.filter(te=instance).delete()

    @receiver(pre_delete, sender=TasksExecution)
    def update_repayment_amount_by_delete_te(sender, instance, **kwargs):
        """
        Метод обновления суммы погашения штрафа за счет задачи te по сигналу pre_delete при её удалении
        """
        repayments = PenaltyRepayment.objects.filter(te=instance)
        penalty_list = []
        for repayment in repayments:
            repayment.penalty.repayment_amount = repayment.penalty.repayment_amount - repayment.repayment_sum
            penalty_list.append(repayment.penalty)
        with transaction.atomic():
            Penalty.objects.bulk_update(penalty_list, ['repayment_amount'])
            repayments.delete()


class PenaltyRepayment(models.Model):
    """
    Модель "Погашение штрафа"
    """
    penalty = models.ForeignKey(Penalty, verbose_name=_('Penalty'), on_delete=models.CASCADE,
                                null=False, blank=False)
    te = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.SET_NULL,
                           null=True, blank=True)
    # Сумма погашения штрафа, полученная от задачи te
    repayment_sum = models.FloatField(_('Сумма погашения'), default=0)

    class Meta:
        db_table = 'survey_penalty_repayment'
        ordering = ['penalty']
        verbose_name = 'Погашение штрафа'
        verbose_name_plural = 'Погашение штрафов'

    def __str__(self):
        return str(self.penalty)


@receiver(pre_delete, sender=PenaltyRepayment)
def update_repayment_amount_by_delete_penalty_repayment(sender, instance, **kwargs):
    """
    Удаление погашения штрафа с откатом погашения и возмещением суммы задачи при удалении погашения.
    """
    instance = PenaltyRepayment.objects.get(id=instance.id)
    with transaction.atomic():
        Penalty.objects.filter(id=instance.penalty.id).update(
            repayment_amount=round(instance.penalty.repayment_amount-instance.repayment_sum, 1)
        )
        TasksExecution.objects.filter(id=instance.te.id).update(
            money=round(instance.te.money+instance.repayment_sum, 1)
        )
