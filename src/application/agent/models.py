from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from application.iceman.models import Stock
from application.loyalty.models import Department, Program
from application.solar_staff_accounts.models import SolarStaffAccount
from application.survey.models import User, UserStatus
from public_model.models import PublicModel
from sort_model.models import OrderModel

from .utils import send_user_status_change


class StoreCategory(models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    default = models.BooleanField(_('Default'), default=False)

    payment_name = models.CharField(_('Payment name'), max_length=100, blank=True, null=True)
    payment_string = models.CharField(_('Payment connection string'), max_length=255, blank=True, null=True)

    telegram_channel_id = models.CharField(_('Telegram channel Id'), max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'agent_stores_categories'
        ordering = ['name']
        verbose_name = _('Store category')
        verbose_name_plural = _('Store categories')

    def __str__(self):
        return '%s' % self.name


class City(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    code = models.CharField(_('Code'), max_length=50, unique=True)
    source = models.CharField(_('Source 1c'), max_length=200, unique=True, null=True, blank=True)
    email = models.TextField(_('E-mail sending orders'), help_text=_('Separated by comma'), null=True, blank=True)

    class Meta:
        db_table = 'agent_cities'
        ordering = ['name']
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return '%s' % self.name


class Category(OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    store_categories = models.ManyToManyField(StoreCategory, verbose_name=_('Store category'),
                                              related_name='good_categories_store_categories', blank=True)

    # DEPRECATE
    only_user = models.ForeignKey(UserStatus, verbose_name=_('Only for user'), on_delete=models.SET_NULL, null=True,
                                  blank=True)
    departments = models.ManyToManyField(Department, verbose_name=_('Departments'),
                                         related_name='good_categories_departments', blank=True)

    class Meta:
        db_table = 'agent_categories'
        ordering = ['order']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return '%s' % self.name

    @cached_property
    def get_departments(self):
        return ", ".join([i.name for i in self.departments.all()])
    get_departments.short_description = _('Departments')

    @cached_property
    def get_store_categories(self):
        return ", ".join([i.name for i in self.store_categories.all()])
    get_store_categories.short_description = _('Store categories')


class Brand(OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200, unique=True)
    cashback_percent = models.FloatField(_('Cashback percent'), default=5, help_text=_('in %'))

    class Meta:
        db_table = 'agent_brands'
        ordering = ['order']
        verbose_name = _('Super group')
        verbose_name_plural = _('Super groups')

    def __str__(self):
        return '%s' % self.name


class Good(OrderModel, PublicModel, models.Model):

    code = models.CharField(_('Code'), max_length=100, unique=True)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    image = models.FileField(_('Image'), upload_to='goods/', null=True, blank=True)

    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'), related_name='good_categories')
    brand = models.ForeignKey(Brand, verbose_name=_('Super group'), on_delete=models.CASCADE)

    url = models.CharField(_('Url'), max_length=1000, blank=True, default='')

    unit = models.CharField(_('Unit'), max_length=100)
    price = models.FloatField(_('Price'))
    box_count = models.IntegerField(_('Box count'), null=True, blank=True)
    min_count = models.IntegerField(_('Minimum count'), null=True, blank=True)

    is_popular = models.BooleanField(_('Is popular'), default=False)
    is_oeskimo = models.BooleanField(_('Is Oeskimo'), default=False)
    is_processed = models.BooleanField(_('Is processed'), default=True)
    is_not_delete = models.BooleanField(_('Is not delete'), default=False)
    is_no_order = models.BooleanField(_('Is no order'), default=False)
    is_only_text = models.BooleanField(_('Is only text'), default=False)

    cashback = models.FloatField(_('Cashback'), blank=True, default=0)
    manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=True, default='')
    brand_name = models.CharField(_('Brand'), max_length=100, blank=True, default='')

    rest = models.IntegerField(_('Rest'), blank=True, null=True)

    class Meta:
        db_table = 'agent_goods'
        ordering = ['category__only_user__id', 'category__order', 'order']
        verbose_name = _('Good')
        verbose_name_plural = _('Goods')

    def __str__(self):
        return '%s' % self.name

    @cached_property
    def get_categories(self):
        return ", ".join([i.name for i in self.categories.all()])
    get_categories.short_description = _('Categories')


class GoodPrice(PublicModel, models.Model):

    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('City'), on_delete=models.CASCADE)
    price = models.FloatField(_('Price'))

    class Meta:
        db_table = 'agent_goods_prices'
        ordering = ['good__name', 'city__name']
        verbose_name = _('Good price')
        verbose_name_plural = _('Good prices')
        unique_together = (('good', 'city'), )

    def __str__(self):
        return 'Price for %s in %s' % (self.good.name, self.city.name)


class GoodPriceType(PublicModel, models.Model):

    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE)
    price_type = models.CharField(_('Price type'), max_length=255, db_index=True)
    price = models.FloatField(_('Price'))
    is_processed = models.BooleanField(_('Is processed'), default=True)

    class Meta:
        db_table = 'agent_goods_prices_types'
        ordering = ['good__name', 'price_type']
        verbose_name = _('Good price')
        verbose_name_plural = _('Good prices')
        unique_together = (('good', 'price_type'), )

    def __str__(self):
        return 'Price for %s type %s' % (self.good.name, self.price_type)


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
        db_table = 'agent_imports'
        ordering = ['-date_start']
        verbose_name = _('Data import')
        verbose_name_plural = _('Data imports')

    def __str__(self):
        return '%s' % self.date_start


class Store(models.Model):

    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    name = models.CharField(_('Name'), max_length=255)
    contact = models.CharField(_('Contact face'), max_length=255, blank=True, default='')
    phone = models.CharField(_('Phone'), max_length=30, blank=True, default='')
    address = models.CharField(_('Address'), max_length=1000, blank=True, default='')
    inn = models.CharField(_('Inn'), max_length=12, blank=True, default='')
    agent = models.CharField(_('Sales Representative'), max_length=1000, blank=True, default='')

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('City'), on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(StoreCategory, verbose_name=_('Category'), on_delete=models.SET_NULL, null=True,
                                 blank=True)

    inn_name = models.CharField(_('Organization name'), max_length=1000, blank=True, default='', null=True)
    inn_full_name = models.CharField(_('Organization full name'), max_length=1000, blank=True, default='', null=True)
    inn_director_title = models.CharField(_('Director title'), max_length=1000, blank=True, default='', null=True)
    inn_director_name = models.CharField(_('Director name'), max_length=1000, blank=True, default='', null=True)
    inn_address = models.CharField(_('Address'), max_length=1000, blank=True, default='', null=True)
    inn_kpp = models.CharField(_('KPP'), max_length=1000, blank=True, default='', null=True)
    inn_ogrn = models.CharField(_('OGRN'), max_length=1000, blank=True, default='', null=True)
    inn_okved = models.CharField(_('OKVED'), max_length=1000, blank=True, default='', null=True)
    inn_region = models.CharField(_('Region'), max_length=1000, blank=True, default='', null=True)

    is_agreement = models.BooleanField(_('Is agreement'), default=False)

    loyalty_department = models.ForeignKey(Department, verbose_name=_('Department'), on_delete=models.SET_NULL,
                                           blank=True, null=True)
    loyalty_program = models.ForeignKey(Program, verbose_name=_('Loyalty program'), on_delete=models.SET_NULL,
                                        blank=True, null=True)
    loyalty_1c_code = models.CharField(_('1c code'), max_length=100, blank=True, null=True)
    loyalty_1c_user = models.CharField(_('1c code user'), max_length=200, blank=True, null=True)

    loyalty_plan = models.FloatField(_('Loyalty plan'), default=0)
    loyalty_fact = models.FloatField(_('Loyalty fact'), default=0)
    loyalty_cashback = models.FloatField(_('Loyalty cashback'), default=0)
    loyalty_sumcashback = models.FloatField(_('Loyalty sumcashback'), default=0)
    loyalty_debt = models.FloatField(_('Loyalty debt'), default=0)
    loyalty_overdue_debt = models.FloatField(_('Loyalty overdue_debt'), default=0)

    loyalty_cashback_payed = models.FloatField(_('Loyalty cashback payed'), default=0)
    loyalty_cashback_to_pay = models.FloatField(_('Loyalty cashback to payed'), default=0)

    is_deleted = models.BooleanField(_('Store deleted'), default=False)

    price_type = models.CharField(_('Price type'), max_length=255, blank=True, null=True)

    stock = models.ForeignKey(Stock, verbose_name='Склад', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'agent_stores'
        ordering = ['-date_create']
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return '%s' % self.name

    @cached_property
    def last_order_id(self):
        order = Order.objects.filter(store=self).last()
        if order:
            return str(order.id)
        else:
            ''

    @cached_property
    def last_order_date(self):
        order = Order.objects.filter(store=self).last()
        if order:
            return str(order.date_order)
        else:
            ''

    @property
    def is_loyalty(self):
        return self.loyalty_department is not None


class Order(models.Model):

    statuses = (
        (1, _('New')),
        (2, _('Payed')),
        (3, _('Pay in Solar')),
        (6, _('Payed cashback')),
        (4, _('Canceled')),
        (5, _('Finished')),
        (7, _('Error payment')),
    )

    payment_types = (
        ('driver', _('Pay to driver')),
        ('telegram', _('Pay via telegram')),
    )

    statuses_1c = (
        ('a', _('Payed')),
        ('b', _('Bonus')),
        ('x', _('Canceled')),
    )

    telegram_channel_types = (
        (0, _('Not need')),
        (1, _('Wait')),
        (2, _('Sent')),
    )

    date_order = models.DateTimeField(_('Date order'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)

    delivery_address = models.CharField(_('Delivery address'), max_length=1000)
    delivery_date = models.DateField(_('Delivery date'))

    sum = models.FloatField(_('Sum'), default=0, blank=True)
    cashback_sum = models.FloatField(_('Cashback sum'), default=0, null=True, blank=True)
    calc_cashback_sum = models.BooleanField(_('Re calc cashback sum'), default=False)

    comment = models.TextField(_('Comment'), max_length=1000)
    comments_status = models.TextField(_('Status comments'), blank=True, default='',
                                       help_text=_('What comes to the user when the status changes'), null=True)

    store = models.ForeignKey(Store, verbose_name=_('For store'), on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(_('Status'), default=1, choices=statuses)
    need_check = models.BooleanField(_('Need check'), default=False)

    telegram_channel_status = models.IntegerField(_('Telegram channel status'), default=1,
                                                  choices=telegram_channel_types)

    from_1c_firm = models.CharField(_('Payment firm'), max_length=100, null=True, blank=True)
    from_1c_sum = models.FloatField(_('1c sum'), null=True, blank=True)
    from_1c_pay = models.FloatField(_('1c pay sum'), null=True, blank=True)
    from_1c_status = models.CharField(_('1c status'), max_length=1, choices=statuses_1c, null=True, blank=True)

    from_1c_cashback = models.FloatField(_('1c cashback'), null=True, blank=True)

    ss_account = models.ForeignKey(SolarStaffAccount, related_name='order_ss_account',
                                   verbose_name=_('Solar staff account'),
                                   on_delete=models.SET_NULL, null=True, blank=True)

    payment_type = models.CharField(_('Payment type'), max_length=20, choices=payment_types, null=True, blank=True)
    payment_status = models.BooleanField(_('Payment status'), default=False)
    payment_sum = models.FloatField(_('Payment sum'), default=0, blank=True)

    __original_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def calc_cashback(self):

        s = 0

        goods = OrderGood.objects.filter(order=self).prefetch_related('brand')
        for i in goods:
            s += i.brand.cashback_percent * i.price * i.count / 100

        self.cashback_sum = round(s)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.calc_cashback_sum:

            self.calc_cashback()
            self.calc_cashback_sum = False

        if self.status != self.__original_status and self.status in [6, 4]:

            # Отправка сообщения
            old_status = 'Нет'
            for i in self.statuses:
                if i[0] == self.__original_status:
                    old_status = i[1]
            send_user_status_change(self, old_status)

        self.__original_status = self.status
        super(Order, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        db_table = 'agent_orders'
        ordering = ['-date_order']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return _('Order %s') % self.id


class OrderGood(models.Model):

    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='goods')

    count = models.IntegerField(_('Count'), default=1)

    code = models.CharField(_('Code'), max_length=100)
    name = models.CharField(_('Name'), max_length=200)

    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name=_('Super group'), on_delete=models.CASCADE)
    good_source = models.ForeignKey(Good, verbose_name=_('Source good'), on_delete=models.SET_NULL, null=True,
                                    blank=True)

    unit = models.CharField(_('Unit'), max_length=100)
    price = models.FloatField(_('Price'))
    sum = models.FloatField(_('Sum'), default=0, blank=True)

    store = models.ForeignKey(Store, verbose_name=_('For store'), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'agent_orders_goods'
        ordering = ['-order__date_order', 'id']
        verbose_name = _('Order good')
        verbose_name_plural = _('Orders goods')

    def __str__(self):
        return '%s' % self.name


class Cart(models.Model):

    store = models.ForeignKey(Store, verbose_name=_('For store'), on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name=_('Good'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    count = models.IntegerField(_('Count'), default=1)

    class Meta:
        db_table = 'agent_cart'
        ordering = ['id']
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart')

    def __str__(self):
        return '%s' % self.id


class Schedule(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100)
    file = models.FileField(_('Schedule file'), upload_to='agent/schedule/')

    class Meta:
        db_table = 'agent_schedules'
        ordering = ['id']
        verbose_name = _('Delivery schedule')
        verbose_name_plural = _('Delivery schedule')

    def __str__(self):
        return '%s' % self.name


class Payment(PublicModel, models.Model):

    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    source = models.CharField(_('Payment source'), max_length=255)
    provider = models.CharField(_('Payment provider'), max_length=255)
    currency = models.CharField(_('Currency'), max_length=3)
    total_amount = models.FloatField(_('Total amount'))
    invoice_payload = models.CharField(_('Order info'), max_length=255)
    telegram_payment_charge_id = models.CharField(_('Telegram payment id'), max_length=255)
    provider_payment_charge_id = models.CharField(_('Provider payment id'), max_length=255)

    class Meta:
        db_table = 'agent_payments'
        ordering = ['-date_create']
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return 'Payment %s' % self.id


class PromoCode(models.Model):

    code = models.CharField(_('Code'), max_length=1000, unique=True)

    is_used = models.BooleanField(_('Is used'), default=False)
    store = models.OneToOneField(Store, related_name='promo_codes_stores', verbose_name=_('Store'),
                                 on_delete=models.SET_NULL, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'agent_promo_codes'
        ordering = ['id']
        verbose_name = _('Promo code')
        verbose_name_plural = _('Promo codes')

    def __str__(self):
        return '%s' % self.code


class TinkoffPayment(models.Model):

    date_create = models.DateTimeField('Date create', auto_now_add=True)
    terminal_key = models.CharField('Terminal key', max_length=1000, null=True, blank=True)
    order_id = models.CharField('Order id', max_length=1000, null=True, blank=True)
    success = models.BooleanField(_('Success'), null=True, blank=True)
    status = models.CharField(_('Status'), null=True, max_length=1000, blank=True)
    payment_id = models.CharField('Payment id', null=True, max_length=1000, blank=True)
    error_code = models.CharField('Error code', null=True, max_length=1000, blank=True)
    amount = models.CharField('Amount', null=True, max_length=1000, blank=True)
    card_id = models.CharField('Card id', null=True, max_length=1000, blank=True)
    pan = models.CharField('Pan', null=True, max_length=1000, blank=True)
    exp_date = models.CharField('Exp date', null=True, max_length=1000, blank=True)

    class Meta:
        db_table = 'agent_payments_tinkoff'
        ordering = ['-date_create']
        verbose_name = _('Tinkoff payment')
        verbose_name_plural = _('Tinkoff payments')

    def __str__(self):
        return '%s' % self.order_id
