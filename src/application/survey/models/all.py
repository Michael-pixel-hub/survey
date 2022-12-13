from application.ai.models import AIProject
from application.solar_staff_accounts.models import SolarStaffAccount
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel
from sort_model.models import OrderModel

from ..utils import get_coordinates


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
    return uuid.uuid4().hex


class Rank(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    default = models.BooleanField(_('Default'), default=False, blank=True)
    work_days = models.IntegerField(_('Work days'), blank=True, default=0)
    tasks_month = models.IntegerField(_('Tasks month count'), blank=True, default=0)
    tasks_count = models.IntegerField(_('Tasks count all'), blank=True, default=0)
    rate = models.FloatField(_('Rate'), default=1)

    class Meta:
        db_table = 'chl_ranks'
        ordering = ['name']
        verbose_name = _('Rank')
        verbose_name_plural = _('Ranks')

    def __str__(self):
        return '%s' % self.name


class UserStatus(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_users_statuses'
        ordering = ['name']
        verbose_name = _('User status')
        verbose_name_plural = _('User statuses')

    def __str__(self):
        return '%s' % self.name


class UserStatusIceman(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    default = models.BooleanField('По умолчанию', default=False)

    class Meta:
        db_table = 'chl_users_statuses_iceman'
        ordering = ['name']
        verbose_name = 'Статус пользователя Айсмен'
        verbose_name_plural = 'Статусы пользователей Айсмен'

    def __str__(self):
        return '%s' % self.name


class Bank(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_banks'
        ordering = ['name']
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return '%s' % self.name


class User(models.Model):

    """
    Модель пользователей телеграм
    """

    legal_statuses = (
        ('self_employed', _('Self-employed')),
        ('other', _('Other')),
    )

    qlik_statuses = (
        ('merchandiser', 'Мерчендайзер'),
        ('surveyor', 'Сюрвеер'),
    )

    types = (
        ('supervisor', 'Супервайзер'),
    )

    telegram_id = models.BigIntegerField(_('Telegram id'), unique=True, null=True, blank=True)
    language_code = models.CharField(_('Language'), max_length=10, blank=True, null=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True, null=True)
    username = models.CharField(_('Telegram username'), max_length=255, blank=True, null=True)

    is_register = models.BooleanField(_('Is register'), default=False)
    is_banned = models.BooleanField(_('Is banned'), default=False)
    is_testing = models.BooleanField(_('Testing mode'), default=False)

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

    rank = models.ForeignKey(Rank, verbose_name=_('Rank'), on_delete=models.SET_NULL, null=True, blank=True)
    is_fixed_rank = models.BooleanField(_('Fixed rank'), default=False)

    is_only_self_tasks = models.BooleanField(_('Only self tasks'), default=False)
    status = models.ForeignKey(UserStatus, verbose_name='Статус сюрвеер', related_name='user_status',
                               on_delete=models.SET_NULL, null=True, blank=True)
    status_agent = models.ForeignKey(UserStatus, verbose_name='Статус агент', related_name='user_status_agent',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    status_iceman = models.ForeignKey(UserStatusIceman, verbose_name='Статус айсмен',
                                      related_name='user_status_iceman', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    status_legal = models.CharField(max_length=100, verbose_name=_('Legal status'), choices=legal_statuses, default='other')
    qlik_status = models.CharField(max_length=100, verbose_name='Статус в Клике', choices=qlik_statuses, blank=True,
                                   null=True)
    type = models.CharField(max_length=100, verbose_name='Тип пользователя', choices=types, blank=True, null=True)

    taxpayer_status = models.BooleanField(_('Taxpayer status'), default=False)
    taxpayer_fio = models.CharField(_('FIO'), max_length=255, null=True, blank=True)
    taxpayer_surname = models.CharField(_('Surname'), max_length=255, null=True, blank=True)
    taxpayer_name = models.CharField(_('User name'), max_length=255, null=True, blank=True)
    taxpayer_patronymic = models.CharField(_('Patronymic'), max_length=255, null=True, blank=True)
    taxpayer_passport = models.CharField(_('Passport'), max_length=255, null=True, blank=True)
    taxpayer_passport_series = models.CharField(_('Passport series'), max_length=255, null=True, blank=True)
    taxpayer_passport_number = models.CharField(_('Passport number'), max_length=255, null=True, blank=True)
    taxpayer_inn = models.CharField(_('INN'), max_length=255, null=True, blank=True)
    taxpayer_email = models.CharField(_('E-mail'), max_length=255, null=True, blank=True)
    taxpayer_phone = models.CharField(_('Phone'), max_length=255, null=True, blank=True)
    taxpayer_date = models.DateTimeField(_('Taxpayer join date'), null=True, blank=True)
    taxpayer_bank_account = models.CharField(_('Bank account'), max_length=255, null=True, blank=True)
    taxpayer_bank = models.ForeignKey(Bank, 'Банк', null=True, blank=True)

    route = models.CharField(_('Route name'), max_length=255, null=True, blank=True)

    save_geo = models.BooleanField('Отслеживать координаты', default=False)
    save_geo_time = models.IntegerField('Периодичность в минутах', default=5)

    worker_bonus_iceman = models.FloatField(
        'Бонус в % для работника', null=True, blank=True,
        help_text='Какой % от стоимости товара выплачивается торговому представителю.')

    __original_status_agent = None

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
        email = '' if self.email is None else f'({self.email.replace("@", " @ ")})'
        if self.name:
            s = f'{self.name} {self.surname} {email}'
        else:
            s = email
        if s == '':
            s = 'Неизвестный пользователь'
        return s

    @property
    def fio(self):
        s = '%s %s' % ('' if self.name is None else str(self.name),
                       '' if self.surname is None else str(self.surname), )
        return s.strip()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_status_agent = self.status_agent_id

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.status_agent_id != self.__original_status_agent:

            from application.agent.models import StoreCategory, Store

            if self.__original_status_agent:
                original_status = UserStatus.objects.get(id=self.__original_status_agent)
            else:
                original_status = None

            category_default = None
            try:
                category_default = StoreCategory.objects.filter(default=True).first()
            except:
                pass

            category_old = None
            if original_status:
                try:
                    category_old = StoreCategory.objects.get(name=original_status.name)
                except StoreCategory.DoesNotExist:
                    pass

            category_new = category_default
            if self.status_agent:
                try:
                    category_new = StoreCategory.objects.get(name=self.status_agent.name)
                except StoreCategory.DoesNotExist:
                    pass

            if category_default:
                old_ids = [category_default.id]
                if category_old:
                    old_ids.append(category_old.id)
                Store.objects.filter(user=self, category__id__in=old_ids).update(category=category_new)
                Store.objects.filter(user=self, category__isnull=True).update(category=category_new)

        super(User, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status_agent = self.status_agent


class UserDevice(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_device_user')
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    date_use = models.DateTimeField(_('Date use'), auto_now=True)
    name = models.CharField(_('Name'), max_length=255, blank=True)
    key = models.CharField(_('Device key'), max_length=255)
    os = models.CharField(_('OS'), max_length=255, blank=True)
    os_version = models.CharField('Версия ОС', max_length=255, default='', blank=True)
    version = models.CharField(_('Version'), max_length=255, default='', blank=True)

    class Meta:
        db_table = 'telegram_users_devices'
        ordering = ['-date_create']
        verbose_name = _('Mobile device')
        verbose_name_plural = _('Mobile devices')

    def __str__(self):
        return '%s' % self.name


class UserGeo(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE,
                             related_name='user_heo_user')
    date = models.DateTimeField(_('Date'))
    longitude = models.FloatField(_('Longitude'))
    latitude = models.FloatField(_('Latitude'))

    class Meta:
        db_table = 'chl_users_geo'
        ordering = ['user_id', 'date']
        verbose_name = 'Координаты пользователя'
        verbose_name_plural = 'Координаты пользователей'

    def __str__(self):
        return 'Геолокация пользователя'


class UserDeviceIceman(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE,
                             related_name='user_device_iceman_user')
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    date_use = models.DateTimeField(_('Date use'), auto_now=True)
    name = models.CharField(_('Name'), max_length=255)
    key = models.CharField(_('Device key'), max_length=255)
    os = models.CharField(_('OS'), max_length=255)
    version = models.CharField(_('Version'), max_length=255, default='')

    class Meta:
        db_table = 'iceman_users_devices'
        ordering = ['-date_create']
        verbose_name = _('Mobile device')
        verbose_name_plural = _('Mobile devices')

    def __str__(self):
        return '%s' % self.name


class UserDelete(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_delete_user')
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    notification_send = models.BooleanField('Отправлено уведомление', default=False)
    notification_date = models.DateTimeField('Дата уведомления', null=True, blank=True)

    class Meta:
        db_table = 'telegram_users_deletes'
        ordering = ['-date_create']
        verbose_name = 'Удаление пользователя'
        verbose_name_plural = 'Удаление пользователей'

    def __str__(self):
        return '%s' % self.user.email


class UserSub(OrderModel, models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_sub_user')
    user_sub = models.ForeignKey(User, verbose_name='Подчиненный', on_delete=models.CASCADE,
                                 related_name='user_sub_user_sub')

    class Meta:
        db_table = 'telegram_users_subs'
        ordering = ['user', 'order']
        verbose_name = 'Подчиненный пользователь'
        verbose_name_plural = 'Подчиненные пользователи'
        unique_together = (('user', 'user_sub'), )

    class OrderMeta:
        fk_fields = ('user', )

    def __str__(self):
        return self.user_sub.email if self.user_sub and self.user_sub.email else '-'


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
    factory_code = models.CharField('Код завода', max_length=1000, blank=True, null=True)

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


class TaskCustomer(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        db_table = 'chl_tasks_customers'
        ordering = ['name']
        verbose_name = _('Task customer')
        verbose_name_plural = _('Tasks customers')

    def __str__(self):
        return '%s' % self.name


class Task(PublicModel, models.Model):

    types = (
        ('default', 'Задание с конструктором'),
        ('sales', 'Задание продажа'),
        ('sales_go', 'Задание продажа ГО'),
        ('payment', 'Задание оплата'),
    )

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
    customer = models.ForeignKey(TaskCustomer, related_name='task_customer', verbose_name=_('Task customer'),
                                 on_delete=models.SET_NULL, null=True, blank=True)
    ss_account = models.ForeignKey(SolarStaffAccount, related_name='task_ss_account',
                                   verbose_name=_('Solar staff account'),
                                   on_delete=models.SET_NULL, null=True, blank=True)

    money = models.FloatField(_('Sum'), default=0)
    money_source = models.FloatField(_('Sum source'), default=0)
    money_fix = models.BooleanField('Фиксировать сумму', default=False)

    is_add_money = models.BooleanField(_('Add value'), default=False)
    add_money = models.FloatField(_('Add sum'), blank=True, null=True)
    add_days = models.IntegerField(_('Add days'), blank=True, null=True)
    is_remove_money = models.BooleanField(_('Remove value'), default=False)
    remove_money = models.FloatField(_('Remove sum'), blank=True, null=True)
    remove_days = models.IntegerField(_('Remove days'), blank=True, null=True)
    remove_ppl = models.IntegerField(_('Remove ppl'), blank=True, null=True)

    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)
    per_week = models.IntegerField(_('How many times a week'), default=0, blank=True, choices=per_weeks)

    is_sales = models.BooleanField(_('Is sales task'), default=False, blank=True)
    is_parse = models.BooleanField(_('Parse by inspector'), default=False, blank=True)

    only_status = models.ForeignKey(UserStatus, related_name='task_user_status', verbose_name=_('Only for user status'),
                                    on_delete=models.SET_NULL, blank=True, null=True)

    disable_loyalty = models.BooleanField(_('Disable if store in loyalty'), default=False, blank=True)

    new_task = models.BooleanField(_('New task with constructor'), default=True)

    application = models.CharField('Проект', max_length=20, default='shop_survey', choices=settings.APPLICATIONS)
    ai_project = models.ForeignKey(AIProject, related_name='task_ai_project', verbose_name='Проект распознавания',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    
    type = models.CharField('Тип задачи', max_length=20, null=True, blank=True, choices=types)
    fix_status = models.BooleanField(
        'Фиксировать статус', default=False,
        help_text='Задачи с фиксированным статусом невозможно менять в интерфейсе администрирования, '
                  'статус для них меняется автоматически'
    )

    class Meta:
        db_table = 'chl_tasks'
        ordering = ['name']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return '%s' % self.name


class TaskQuestionnaire(models.Model):

    name = models.CharField(_('Name'), max_length=200)

    class Meta:
        db_table = 'chl_tasks_questionnaires'
        ordering = ['name']
        verbose_name = _('Questionnaire')
        verbose_name_plural = _('Questionnaires')

    def __str__(self):
        return '%s' % self.name


class TaskQuestionnaireQuestion(PublicModel, OrderModel, models.Model):

    types = (
        ('string', _('String')),
        ('integer', _('Integer')),
        ('choices', _('Choices')),
    )

    name = models.CharField(_('Name'), max_length=200)
    question = models.CharField(_('Question text'), max_length=1000)
    choices = models.TextField(_('Choices'), help_text=_('Enter separated'), default='', blank=True)
    require = models.BooleanField(_('Require'), default=True)
    questionnaire = models.ForeignKey(TaskQuestionnaire, related_name='%(app_label)s_%(class)s_task',
                                      verbose_name=_('Questionnaire'), on_delete=models.CASCADE)
    question_type = models.CharField(_('Question type'), max_length=20, default='string', choices=types)

    class Meta:
        db_table = 'chl_tasks_questionnaires_questions'
        ordering = ['questionnaire', 'order']
        verbose_name = _('Questionnaire question')
        verbose_name_plural = _('Questionnaires questions')
        unique_together = (('name', 'questionnaire'), )

    class OrderMeta:
        fk_fields = ('questionnaire', )

    def __str__(self):
        return '%s' % self.name


class TaskStep(PublicModel, OrderModel, models.Model):

    types = (
        ('photos', _('Photos')),
        ('comment', _('Comment')),
        ('questionnaire', _('Questionnaire')),
    )

    task = models.ForeignKey(Task, related_name='%(app_label)s_%(class)s_task', verbose_name=_('Task'),
                             on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=200)
    text = models.TextField(_('Text'))
    step_type = models.CharField(_('Step type'), max_length=20, default='photos', choices=types)
    require = models.BooleanField(_('Require'), default=True)

    photo_inspector = models.BooleanField(_('Parse photo in inspector'), default=False)
    photo_check_assortment = models.BooleanField(_('Check assortment after parse'), default=False)
    photo_check = models.BooleanField(_('Check photo by manager'), default=False)
    photo_from_gallery = models.BooleanField(_('Ability to upload photos from the gallery'), default=True)
    photo_out_reason = models.BooleanField('Указать причины отсутствия', default=False)
    photo_out_requires = models.BooleanField('Причины отсутствия обязательны', default=False)

    questionnaire = models.ForeignKey(TaskQuestionnaire, related_name='%(app_label)s_%(class)s_questionnaire',
                                      verbose_name=_('Questionnaire'), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'chl_tasks_steps'
        ordering = ['task', 'order']
        verbose_name = _('Task step')
        verbose_name_plural = _('Tasks step')
        unique_together = (('name', 'task'), )

    class OrderMeta:
        fk_fields = ('task', )

    def __str__(self):
        return '%s' % self.name


class Assortment(PublicModel, models.Model):

    good = models.ForeignKey(Good, related_name='assortment_good', verbose_name=_('Good'), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='assortment_store', verbose_name=_('Store'), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='assortment_task', verbose_name=_('Task'), on_delete=models.SET_NULL,
                             null=True, blank=True)
    count = models.IntegerField(_('Count'), null=True, blank=True)
    is_delete = models.BooleanField(_('Delete'), default=False)

    class Meta:
        db_table = 'chl_assortment'
        ordering = ['good__name', 'store__client__name', 'store__code']
        verbose_name = _('Store good')
        verbose_name_plural = _('Assortment')
        unique_together = ('good', 'store', 'task')

    def __str__(self):
        return '%s - %s' % (self.good.name, self.store.client.name)


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


class StoreTask(models.Model):

    task = models.ForeignKey(Task, verbose_name=_('Task'), on_delete=models.CASCADE, related_name='store_task_task')
    store = models.ForeignKey(Store, verbose_name=_('Store'), on_delete=models.CASCADE, related_name='store_task_store')
    per_week = models.IntegerField(_('How many times a week'), default=0, blank=True, choices=per_weeks)
    per_month = models.IntegerField(_('How many times a month'), blank=True, null=True)
    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')
    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)
    hours_start = models.IntegerField(_('Hours start'), blank=True, null=True)
    hours_end = models.IntegerField(_('Hours end'), blank=True, null=True)
    only_user = models.ForeignKey(User, verbose_name=_('Only user'), on_delete=models.SET_NULL,
                                  related_name='store_task_user', blank=True, null=True)
    telegram_channel_id = models.CharField(_('Telegram channel id'), max_length=100, blank=True, null=True)

    is_add_value = models.BooleanField(_('Is add value'), default=False, blank=True)
    add_value = models.FloatField(_('New value'), blank=True, null=True)

    position = models.IntegerField('Последовательность', blank=True, null=True)

    class Meta:
        db_table = 'chl_stores_tasks'
        ordering = ['task__name', 'store__client__name', 'store__code']
        verbose_name = _('Store task')
        verbose_name_plural = _('Stores tasks')
        unique_together = ('task', 'store')

    def __str__(self):
        return '%s %s' % (self.task, self.store)

    def save(self, *args, **kwargs):

        if self.per_week == '':
            self.per_week = 0

        if self.per_month == '' or self.per_month == 0:
            self.per_month = None

        super().save(*args, **kwargs)


class UploadRequests(models.Model):

    request_date = models.DateTimeField(_('Request date'), auto_now_add=True)
    request_method = models.CharField(_('Request method'), blank=True, default='', max_length=1000)
    request_type = models.CharField(_('Request type'), blank=True, default='', max_length=1000)
    request_ip = models.CharField(_('Request ip'), blank=True, default='', max_length=1000)
    request_text = models.TextField(_('Request text'), blank=True, default='')
    request_files = models.TextField(_('Request files'), blank=True, default='')

    request_data_type = models.CharField(_('Request data type'), blank=True, default='', max_length=100)
    request_data_count = models.IntegerField(_('Request data count'), blank=True, null=True)

    processed = models.BooleanField(_('Processed'), default=False)
    result = models.TextField(_('Result'), blank=True, default='')

    class Meta:
        db_table = 'survey_1c_requests'
        ordering = ['-request_date']
        verbose_name = _('1c request')
        verbose_name_plural = _('1c requests')

    def __str__(self):
        return '%s %s %s' % (self.request_date, self.request_method, self.request_ip)


class ExternalRequests(models.Model):

    request_date = models.DateTimeField(_('Request date'), auto_now_add=True)
    request_method = models.CharField(_('Request method'), blank=True, default='', max_length=1000)
    request_type = models.CharField(_('Request type'), blank=True, default='', max_length=1000)
    request_ip = models.CharField(_('Request ip'), blank=True, default='', max_length=1000)
    request_text = models.TextField(_('Request text'), blank=True, default='')
    request_files = models.TextField(_('Request files'), blank=True, default='')

    request_data_type = models.CharField(_('Request data type'), blank=True, default='', max_length=100)
    request_data_count = models.IntegerField(_('Request data count'), blank=True, null=True)

    processed = models.BooleanField(_('Processed'), default=False)
    result = models.TextField(_('Result'), blank=True, default='')

    class Meta:
        db_table = 'survey_requests_external'
        ordering = ['-request_date']
        verbose_name = _('External request')
        verbose_name_plural = _('External requests')

    def __str__(self):
        return '%s %s %s' % (self.request_date, self.request_method, self.request_ip)


class Request(models.Model):

    date = models.DateTimeField(_('Request date'), auto_now_add=True)
    method = models.CharField(_('Request method'), blank=True, default='', max_length=1000)
    url = models.TextField(_('Url'), blank=True, default='')
    body = models.TextField(_('Request text'), blank=True, default='')
    result = models.TextField(_('Result'), blank=True, default='')

    class Meta:
        db_table = 'survey_requests'
        ordering = ['-date']
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')

    def __str__(self):
        return '%s %s' % (self.date, self.method)


class Sms(models.Model):

    date = models.DateTimeField(_('Send date'))
    phone = models.CharField(_('Phone'), max_length=100)
    code = models.CharField(_('Code'), max_length=4)
    text = models.TextField(_('Text'))
    response_code = models.IntegerField(_('Response code'), default=200)
    response_text = models.TextField(_('Response text'), default='')

    class Meta:
        db_table = 'survey_sms'
        ordering = ['-date']
        verbose_name = _('Sms')
        verbose_name_plural = _('Sms')

    def __str__(self):
        return '%s %s' % (self.date, self.phone)


class SmsAttempt(models.Model):

    phone = models.CharField(_('Phone'), max_length=100, unique=True)
    attempts = models.IntegerField(_('Attempts count'), default=0)

    class Meta:
        db_table = 'survey_sms_attempts'
        ordering = ['id']
        verbose_name = _('Sms attempt')
        verbose_name_plural = _('Sms attempts')

    def __str__(self):
        return '%s %s' % (self.phone, self.attempts)


class OutReason(OrderModel, PublicModel, models.Model):

    name = models.CharField('Название', max_length=100, unique=True)
    is_report = models.BooleanField('Отправлять в качестве проблемы', default=False)

    class Meta:
        db_table = 'survey_out_reasons'
        ordering = ['order']
        verbose_name = 'Причина отсутствия'
        verbose_name_plural = 'Причины отсутствия'

    def __str__(self):
        return self.name
