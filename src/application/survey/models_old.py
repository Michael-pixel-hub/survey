import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _

from public_model.models import PublicModel
from django.contrib.auth.models import AbstractBaseUser

from .utils import get_coordinates, send_user_status_change

per_weeks = (
    (0, _('Not limited')),
    (1, _('Once a week')),
    (2, _('2 times per week')),
    (3, _('3 times per week')),
    (4, _('4 times per week')),
    (5, _('5 times per week')),
    (6, _('6 times per week')),
)


def gen_key():
    import uuid
    while True:
        key = uuid.uuid4().hex
        try:
            User.objects.get(api_key=key)
        except User.DoesNotExist:
            return key


class User(models.Model):
    """
    Модель пользователей телеграм
    """

    telegram_id = models.IntegerField(_('Telegram id'), unique=True, null=True, blank=True)
    language_code = models.CharField(_('Language'), max_length=10, blank=True, null=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True, null=True)
    username = models.CharField(_('Telegram username'), max_length=255, blank=True, null=True)

    is_register = models.BooleanField(_('Is register'), default=False)
    is_banned = models.BooleanField(_('Is banned'), default=False)

    phone = models.CharField(_('Phone'), max_length=100, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True)
    surname = models.CharField(_('Surname'), max_length=100, blank=True, null=True)

    advisor = models.CharField(_('Advisor fio'), max_length=255, blank=True, null=True)

    bank_card = models.CharField(_('Bank card'), max_length=100, blank=True, null=True)
    e_money = models.CharField(_('Online wallet'), max_length=100, blank=True, null=True)

    money = models.FloatField(_('Balance'), blank=True, default=0)

    email = models.CharField(_('E-mail'), blank=True, null=True, max_length=100)
    city = models.CharField(_('City/Region'), blank=True, null=True, max_length=100)

    date_join = models.DateTimeField(_('Date join'), auto_now_add=True)

    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)

    static_longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    static_latitude = models.FloatField(_('Latitude'), null=True, blank=True)

    is_need_solar_staff_reg = models.BooleanField(_('Need Solar staff register'), default=False)

    api_key = models.CharField(_('API key'), blank=True, null=True, max_length=32, default=gen_key, unique=True)
    source = models.CharField(_('Source'), max_length=100, default=_('Telegram'), db_index=True)

    class Meta:
        db_table = 'telegram_users'
        ordering = ['-date_join']
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['name']),
            models.Index(fields=['surname']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        s = ''
        if self.last_name:
            if self.first_name:
                s = '%s %s' % (self.first_name, self.last_name)
            else:
                s = '%s' % self.last_name
        else:
            if self.first_name:
                s = '%s' % self.first_name
        if self.username:
            s = '%s @%s' % (s, self.username)
        if s == '':
            if self.name:
                s = '%s %s' % (self.name, self.surname)
        return s

    @property
    def fio(self):
        s = '%s %s' % ('' if self.first_name is None else str(self.first_name),
                       '' if self.last_name is None else str(self.last_name), )
        return s.strip()


class Client(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_clients'
        ordering = ['name']
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return '%s' % self.name


class Category(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_categories'
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return '%s' % self.name


class Region(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_regions'
        ordering = ['name']
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return '%s' % self.name


class Store(PublicModel, models.Model):

    client = models.ForeignKey(Client, related_name='client_store', verbose_name=_('Chain stores'),
                               on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_store', verbose_name=_('Category'),
                                 on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=100, blank=True, unique=True)
    region = models.CharField(_('Region'), max_length=100, blank=True)
    region_o = models.ForeignKey(Region,  verbose_name=_('Region'), null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(_('Address'), max_length=500, blank=True)

    auto_coord = models.BooleanField(_('Auto calc coordinates'), default=False)
    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)

    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')

    class Meta:
        db_table = 'chl_stores'
        ordering = ['client__name', 'code']
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')
        indexes = [
            models.Index(fields=['address']),
        ]

    def __str__(self):
        return '%s - %s - %s' % (self.code, self.client.name, self.address)

    def save(self, *args, **kwargs):

        if self.auto_coord and self.address:

            self.longitude, self.latitude = get_coordinates(self.address)
            self.auto_coord = False

        super(Store, self).save(*args, **kwargs)


class Good(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.FileField(_('Image'), upload_to='goods/', null=True, blank=True)
    code = models.CharField(_('Code'), max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'chl_goods'
        ordering = ['name']
        verbose_name = _('Good')
        verbose_name_plural = _('Production')

    def __str__(self):
        return '%s' % self.name


class Assortment(PublicModel, models.Model):

    good = models.ForeignKey(Good, related_name='assortment_good', verbose_name=_('Good'), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='assortment_store', verbose_name=_('Store'), on_delete=models.CASCADE)

    class Meta:
        db_table = 'chl_assortment'
        ordering = ['good__name', 'store__client__name', 'store__code']
        verbose_name = _('Store good')
        verbose_name_plural = _('Assortment')
        unique_together = ('good', 'store')

    def __str__(self):
        return '%s - %s' % (self.good.name, self.store.client.name)


class Task(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'))
    instruction = models.FileField(_('Instruction file'), upload_to='instructions/', null=True, blank=True)
    instruction_url = models.CharField(_('Instruction url'), blank=True, max_length=100)

    clients = models.ManyToManyField(Client, related_name='task_clients', verbose_name=_('Clients'), blank=True)
    stores = models.ManyToManyField(Store, related_name='task_stores', verbose_name=_('Stores'), blank=True)
    regions = models.ManyToManyField(Region, related_name='task_regions', verbose_name=_('Regions'), blank=True)

    client = models.ForeignKey(Client, related_name='task_client', verbose_name=_('Client'), on_delete=models.SET_NULL,
                               null=True, blank=True)
    store = models.ForeignKey(Store, related_name='task_store', verbose_name=_('Store'), on_delete=models.SET_NULL,
                              null=True, blank=True)
    money = models.FloatField(_('Sum'), default=0)

    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)
    per_week = models.IntegerField(_('How many times a week'), default=0, blank=True, choices=per_weeks)

    is_sales = models.BooleanField(_('Is sales task'), default=False, blank=True)
    is_parse = models.BooleanField(_('Parse by inspector'), default=False, blank=True)

    class Meta:
        db_table = 'chl_tasks'
        ordering = ['name']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return '%s' % self.name


class TasksExecution(models.Model):

    statuses = (
        (1, _('Started')),
        (2, _('Finished')),
        (3, _('Checked')),
        (6, _('Pay in Solar')),
        (4, _('Payed')),
        (5, _('Denied')),
        (7, _('Not payed')),
    )

    inspector_statuses = (
        ('undefined', _('Undefined')),
        ('wait', _('Waiting for inspector')),
        ('upload_error', _('Upload error')),
        ('parse_error', _('Parse error')),
        ('report_error', _('Report error')),
        ('report_wait', _('Report waiting')),
        ('error', _('Error')),
        ('success', _('Success parsing')),
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
    )

    user = models.ForeignKey(User, related_name='task_user', verbose_name=_('User'), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task', verbose_name=_('Task'), on_delete=models.CASCADE)

    date_start = models.DateTimeField(_('Date start'), auto_now_add=True)
    date_end = models.DateTimeField(_('Date end'), null=True, blank=True)
    status = models.IntegerField(_('Status'), default=1, choices=statuses)

    store = models.ForeignKey(Store, related_name='task_e_store', verbose_name=_('Store'), on_delete=models.SET_NULL,
                              null=True, blank=True)

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
    check_type = models.CharField(_('Check'), default='not_verified', choices=check_types, max_length=12)
    set_check_verified = models.BooleanField(_('Set check verified'), blank=True, default=False)
    set_check_not_verified = models.BooleanField(_('Set check not verified'), blank=True, default=False)
    is_auditor = models.BooleanField(_('Checked by auditor'), blank=True, default=False)
    check_user = models.ForeignKey(AbstractBaseUser, verbose_name=_('Check user'), on_delete=models.SET_NULL,
                                   null=True, blank=True)

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

    __original_status = None

    class Meta:
        db_table = 'chl_tasks_executions'
        ordering = ['-date_start']
        verbose_name = _('Task execution')
        verbose_name_plural = _('Tasks execution')
        indexes = [
            models.Index(fields=['comments']),
        ]

    def __str__(self):
        return '%s %s' % (self.user, self.task)

    def __init__(self, *args, **kwargs):
        super(TasksExecution, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.set_check_not_verified:
            self.check_type = 'false'
            self.set_check_not_verified = False

        if self.set_check_verified:
            self.check_type = 'true'
            self.set_check_verified = False

        if self.status != self.__original_status and self.status == 6:

            pass

            # Платеж
            #from application.survey.solar_staff.tasks import solar_staff_pay
            #solar_staff_pay.apply_async((self.id, ), countdown=60)

        if self.status != self.__original_status and self.status in [3, 4, 5]:

            # Отправка сообщения
            old_status = 'Нет'
            for i in self.statuses:
                if i[0] == self.__original_status:
                    old_status = i[1]
            send_user_status_change(self, old_status)

        super(TasksExecution, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    def user_name(self):
        return self.user.name
    user_name.short_description = _('Name')

    def user_surname(self):
        return self.user.surname
    user_surname.short_description = _('Surname')


class TasksExecutionCheck(TasksExecution):
    class Meta:
        proxy = True
        verbose_name = _('Task execution check')
        verbose_name_plural = _('Tasks execution checks')


class TasksExecutionImage(models.Model):

    image_types = (
        ('undefined', _('Undefined')),
        ('enter', _('Enter photo')),
        ('before', _('Photo before work')),
        ('after', _('Photo after work')),
        ('check', _('Cass check')),
    )

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='task_images')
    image = models.FileField(_('Image'), upload_to='tasks/exec/%Y/%m/%d/', null=True, blank=True,
                             db_index=True)
    status = models.CharField(_('Unique status'), max_length=1000, default=str(_('Image analysis in progress...')),
                              db_index=True)
    md5 = models.CharField('Md5 sum', max_length=32, blank=True, null=True)

    type = models.CharField(_('Image type'), max_length=10, default='undefined', choices=image_types)

    class Meta:
        db_table = 'chl_tasks_executions_images'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Confirmation image')
        verbose_name_plural = _('Confirmation images')

    def __str__(self):
        return '%s' % self.image.path

    def save(self, *args, **kwargs):

        md5sum = hashlib.md5(open(self.image.path, 'rb').read()).hexdigest()
        self.md5 = md5sum
        super(TasksExecutionImage, self).save(*args, **kwargs)


class Agreement(models.Model):

    name = models.CharField(_('Name'), max_length=100)
    file = models.FileField(_('Agreement file'), upload_to='agreements/')

    class Meta:
        db_table = 'chl_agreements'
        ordering = ['id']
        verbose_name = _('Agreement')
        verbose_name_plural = _('Agreement')

    def __str__(self):
        return '%s' % self.name


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

    class Meta:
        db_table = 'chl_imports'
        ordering = ['-date_start']
        verbose_name = _('Data import')
        verbose_name_plural = _('Data imports')

    def __str__(self):
        return '%s' % self.date_start


class StoreTask(models.Model):

    task = models.ForeignKey(Task, verbose_name=_('Task'), on_delete=models.CASCADE, related_name='store_task_task')
    store = models.ForeignKey(Store, verbose_name=_('Store'), on_delete=models.CASCADE, related_name='store_task_store')
    per_week = models.IntegerField(_('How many times a week'), default=0, blank=True, choices=per_weeks)
    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')
    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)
    hours_start = models.IntegerField(_('Hours start'), blank=True, null=True)
    hours_end = models.IntegerField(_('Hours end'), blank=True, null=True)

    class Meta:
        db_table = 'chl_stores_tasks'
        ordering = ['task__name', 'store__client__name', 'store__code']
        verbose_name = _('Store task')
        verbose_name_plural = _('Stores tasks')
        unique_together = ('task', 'store')

    def __str__(self):
        return '%s %s' % (self.task, self.store)


class TasksExecutionAssortment(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='tea_task')
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE, related_name='tea_good')
    avail = models.FloatField(_('Avail'))

    class Meta:
        db_table = 'chl_tasks_executions_assortment'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment')
        verbose_name_plural = _('Avail assortments')

    def __str__(self):
        return '%s' % self.good


class TasksExecutionAssortmentBefore(models.Model):

    task = models.ForeignKey(TasksExecution, verbose_name=_('Task execution'), on_delete=models.CASCADE,
                             related_name='tea_task_b')
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE, related_name='tea_good_b')
    avail = models.FloatField(_('Avail'))

    class Meta:
        db_table = 'chl_tasks_executions_assortment_before'
        ordering = ['-task__date_start', 'id']
        verbose_name = _('Avail assortment before')
        verbose_name_plural = _('Avail assortments before')

    def __str__(self):
        return '%s' % self.good
