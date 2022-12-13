from application.survey.models import User, Task
from application.survey.utils import get_coordinates
from datetime import date, timedelta
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from public_model.models import PublicModel
from sort_model.models import OrderModel

from .dadata import fill_inn_data

categories = (
    ('important', _('Important message')),
    ('task', _('Task')),
    ('act', _('Act')),
)


class Notification(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, null=True, blank=True,
                             related_name='iceman_user')
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    title = models.CharField(_('Title'), max_length=255)
    message = models.TextField(_('Message'))
    category = models.TextField(_('Category'), max_length=20, default='important', choices=categories)

    is_sent = models.BooleanField(_('Is sent'), default=False)

    result = models.TextField(_('Result'), default='', blank=True)

    class Meta:
        db_table = 'iceman_notifications'
        ordering = ['-date_create']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return '%s #%s' % (_('Notification'), self.id)


class Source(models.Model):

    name = models.CharField('Название', max_length=255, unique=True)
    sys_name = models.CharField('Системное имя', max_length=255, unique=True)

    discount = models.FloatField('Скидка оплаты по факту в %', default=5,
                                 help_text='Процент скидки при выборе оплаты по факту. 0 - нет скидки.', blank=True)
    fact_text = models.TextField('Текст оплаты по факту', default='', help_text='{discount} - скидка', blank=True)

    payment_days = models.IntegerField('Кол-во дней отсрочки', default=10, blank=True)
    sum_restrict = models.FloatField('Ограничение суммы в руб.', default=4000,
                                     help_text='Ограничение суммы в рублях при отсрочки. 0 - нет ограничения.',
                                     blank=True)
    delay_text = models.TextField('Текст отсрочки', default='', blank=True,
                                  help_text='{days} - кол-во дней, {sum} - ограничение суммы')

    bonus = models.FloatField('Бонус в %', default=20,
                              help_text='На сколько процентов от суммы товаров можно приобрести в качестве '
                                        'бонуса. 0 - нет бонуса.', blank=True)
    delivery_max_days = models.IntegerField('Число дней доставки', default=10,
                                            help_text='Максимальное число дней доставки')
    worker_bonus = models.FloatField('Бонус в % для работника', default=8,
                                     help_text='Какой % от стоимости товара выплачивается торговому представителю.')

    email = models.CharField('E-mail отправки заказов', max_length=255, default='', blank=True)
    telegram_id = models.CharField('Телеграм id отправки заказов в Айсман', max_length=255, default='', blank=True)
    go_telegram_id = models.CharField('Телеграм id отправки заказов в ГО', max_length=255, default='', blank=True)

    partner_name = models.CharField('Название партнера', max_length=255, default='', blank=True)
    partner_email = models.CharField('E-mail партнера', max_length=255, default='', blank=True)
    partner_fio = models.CharField('ФИО партнера', max_length=255, default='', blank=True)
    partner_phone = models.CharField('Телефон партнера', max_length=255, default='', blank=True)

    class Meta:
        db_table = 'iceman_sources'
        ordering = ['name']
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.name


class Stock(models.Model):

    name = models.CharField('Название', max_length=255)
    sys_name = models.CharField('Системное имя', max_length=255, unique=True)
    default = models.BooleanField('По умолчанию', default=False)
    source = models.ForeignKey(Source, verbose_name='Источник', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'iceman_stocks'
        ordering = ['name']
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class Region(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    short_name = models.CharField('Короткое название', max_length=100, unique=True)
    short_name_2 = models.CharField('Короткое название', max_length=100, unique=True, blank=True, null=True)
    stock = models.ForeignKey(Stock, verbose_name='Склад', on_delete=models.SET_NULL, blank=True, null=True)
    name_1c = models.CharField('Название в 1с', max_length=100, unique=True, blank=True, null=True)
    name_1c_2 = models.CharField('Название в 1с', max_length=100, unique=True, blank=True, null=True)
    source = models.ForeignKey(Source, verbose_name='Источник', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'iceman_regions'
        ordering = ['name']
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return '%s' % self.name


class Store(PublicModel, models.Model):

    types = (
        ('iceman', 'Айсмен'),
        ('go', 'Городской отдел'),
        ('client', 'Клиентский'),
    )

    date_create = models.DateTimeField('Дата создания', blank=True, null=True)

    name = models.CharField('Название', max_length=255)

    code = models.CharField('Код', max_length=100, blank=True, unique=True, null=True)
    region = models.ForeignKey(Region,  verbose_name='Регион', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='iceman_store_region')
    address = models.TextField('Адрес', max_length=500, blank=True)

    auto_coord = models.BooleanField('Автоматически определить координаты', default=False)

    longitude = models.FloatField('Долгота', null=True, blank=True)
    latitude = models.FloatField('Широта', null=True, blank=True)

    inn = models.CharField('ИНН', max_length=12, blank=True, default='')
    inn_auto = models.BooleanField('Автоматически загрузить данные', default=False)

    type = models.CharField('Тип магазина', max_length=20, choices=types, default='iceman')

    inn_name = models.CharField('Название организации', max_length=1000, blank=True, default='', null=True)
    inn_name_1 = models.CharField('Полное название организации', max_length=1000, blank=True, default='', null=True)
    inn_director_title = models.CharField('Должность директора', max_length=1000, blank=True, default='', null=True)
    inn_director_name = models.CharField('Фио директора', max_length=1000, blank=True, default='', null=True)
    inn_address = models.CharField('Адрес', max_length=1000, blank=True, default='', null=True)
    inn_kpp = models.CharField('КПП', max_length=1000, blank=True, default='', null=True)
    inn_ogrn = models.CharField('ОГРН', max_length=1000, blank=True, default='', null=True)
    inn_okved = models.CharField('ОКВЭД', max_length=1000, blank=True, default='', null=True)
    inn_type = models.CharField('Тип организации', max_length=1000, blank=True, default='', null=True)
    inn_region = models.CharField(_('Region'), max_length=1000, blank=True, default='', null=True)

    is_agreement = models.BooleanField('Заключен договор', default=False)
    is_agreement_data = models.BooleanField('Данные для договора', default=False)

    lpr_phone = models.CharField('Телефон продавца', max_length=255, blank=True, default='', null=True)
    lpr_fio = models.CharField('ФИО продавца', max_length=255, blank=True, default='', null=True)
    director_phone = models.CharField('Телефон директора', max_length=255, blank=True, default='', null=True)
    director_fio = models.CharField('ФИО директора', max_length=255, blank=True, default='', null=True)

    price_type = models.CharField('Тип цены', max_length=255, blank=True, null=True)

    photo = models.ImageField('Изображение магазина', upload_to='iceman/stores/photos/%Y/%m/%d/', blank=True, null=True)

    source = models.ForeignKey(Source,  verbose_name='Источник', on_delete=models.CASCADE,
                               related_name='iceman_store_source')

    schedule = models.CharField('Дни доставки', max_length=1000, blank=True, default='')
    payment_days = models.IntegerField('Кол-во дней отсрочки', blank=True, null=True)

    sum_restrict = models.FloatField('Ограничение суммы в руб.', default=0,
                                     help_text='Ограничение суммы в рублях при отсрочки. 0 - нет ограничения.',
                                     blank=True)

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='iceman_store_user')

    is_order_task = models.BooleanField('Задача продажи', default=True)
    is_entry = models.BooleanField('Провод', null=True, blank=True)

    class Meta:
        db_table = 'iceman_stores'
        ordering = ['code']
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        indexes = [
            models.Index(fields=['address']),
        ]

    def __str__(self):
        if self.code:
            return f'{self.code} - {self.name}'
        return self.name

    def save(self, *args, **kwargs):

        if self.auto_coord and self.address:

            self.longitude, self.latitude = get_coordinates(self.address)
            self.auto_coord = False

        if self.inn_auto and self.inn:
            fill_inn_data(self)
            self.inn_auto = False

        super().save(*args, **kwargs)

    @property
    def documents(self):
        return StoreDocument.objects.filter(store=self)

    @property
    def store_id(self):
        return f'ICMS{self.id}'
    store_id.fget.short_description = 'Ид'


class Document(models.Model):

    name = models.CharField('Название', max_length=255)
    sys_name = models.CharField('Системное имя', max_length=255, unique=True)
    description = models.TextField('Описание', default='', blank=True)

    class Meta:
        db_table = 'iceman_documents'
        ordering = ['name']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class DocumentGroup(models.Model):

    name = models.CharField('Название', max_length=255)
    sys_name = models.CharField('Системное имя', max_length=255, unique=True)

    class Meta:
        db_table = 'iceman_documents_groups'
        ordering = ['name']
        verbose_name = 'Группа документов'
        verbose_name_plural = 'Группы документов'

    def __str__(self):
        return self.name


class DocumentGroupDocument(OrderModel, PublicModel, models.Model):

    document = models.ForeignKey(Document, verbose_name='Документ', on_delete=models.CASCADE)
    group = models.ForeignKey(DocumentGroup, verbose_name='Группа документов', on_delete=models.CASCADE)
    required = models.BooleanField('Обязательно', default=True)

    class Meta:
        db_table = 'iceman_documents_groups_documents'
        ordering = ['group__name', 'order']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документ'
        unique_together = (('document', 'group'), )

    class OrderMeta:
        fk_fields = ('group', )

    def __str__(self):
        return self.document.name


class StoreDocument(models.Model):

    types = (
        ('agreement_card', 'Карточка клиента'),
        ('agreement_charter', 'Устав предприятия'),
        ('agreement_director', 'Назначение ген. директора'),
        ('agreement_photo', 'Договор аренды помещения'),
        ('document', 'Фото документа'),
    )

    type = models.CharField('Тип документа', max_length=50, choices=types)
    document = models.ForeignKey(Document, verbose_name='Документ', on_delete=models.SET_NULL,
                                 related_name='iceman_store_document_document', null=True, blank=True)

    number = models.IntegerField('Страница', default=1)
    file = models.ImageField('Изображение документа', upload_to='iceman/stores/documents/%Y/%m/%d/')
    date_create = models.DateTimeField('Дата загрузки', auto_now_add=True)

    store = models.ForeignKey(Store, verbose_name='Магазин', on_delete=models.CASCADE,
                              related_name='iceman_store_document_store')

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                             related_name='iceman_store_document_user')

    class Meta:
        db_table = 'iceman_stores_documents'
        ordering = ['store_id', 'type', 'number']
        verbose_name = 'Документ магазина'
        verbose_name_plural = 'Документы магазина'

    def __str__(self):
        return f'{self.type}, страница {self.number}'


class StoreStock(models.Model):

    store = models.ForeignKey(Store, verbose_name='Магазин', on_delete=models.CASCADE,
                              related_name='iceman_store_stock_store')
    stock = models.ForeignKey(Stock, verbose_name='Склад', on_delete=models.CASCADE)

    class Meta:
        db_table = 'iceman_stores_stocks'
        ordering = ['store_id', 'stock_id']
        verbose_name = 'Склад магазина'
        verbose_name_plural = 'Склады магазина'
        unique_together = (('store', 'stock'), )

    def __str__(self):
        return f'Склад {self.stock.name} магазина {self.store.name}'


class Brand(OrderModel, PublicModel, models.Model):

    name = models.CharField('Название', max_length=200, unique=True)

    class Meta:
        db_table = 'iceman_brands'
        ordering = ['order']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Category(OrderModel, PublicModel, models.Model):

    name = models.CharField('Название', max_length=200, unique=True)

    class Meta:
        db_table = 'iceman_categories'
        ordering = ['order']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name


class Product(OrderModel, PublicModel, models.Model):

    code = models.CharField('Код', max_length=100)
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True, default='')
    image = models.FileField('Изображение', upload_to='iceman/products/', null=True, blank=True)

    categories = models.ManyToManyField(Category, verbose_name='Разделы')
    brand = models.ForeignKey(Brand, verbose_name='Производитель', on_delete=models.CASCADE)

    unit = models.CharField('Ед. измерения', max_length=100)
    box_count = models.IntegerField('Кол-во в коробке', default=1)
    min_count = models.IntegerField('Минимальное количество', default=1)

    price = models.FloatField('Цена', default=0)

    barcode = models.CharField('Штрихкод', max_length=15, default='', unique=True)
    weight = models.IntegerField('Вес в граммах', null=True, blank=True)

    class Meta:
        db_table = 'iceman_products'
        ordering = ['order']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    @cached_property
    def get_categories(self):
        return ", ".join([i.name for i in self.categories.all()])
    get_categories.short_description = 'Категории'


class SourceProduct(OrderModel, PublicModel, models.Model):

    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    source = models.ForeignKey(Source, verbose_name='Источник', on_delete=models.CASCADE)

    unit = models.CharField('Ед. измерения', max_length=100)
    box_count = models.IntegerField('Кол-во в коробке', default=1)
    min_count = models.IntegerField('Минимальное количество', default=1)

    price = models.FloatField('Цена', default=0)
    is_bonus = models.BooleanField('Бонусный товар', default=False)

    is_updated = models.BooleanField('Обновлен', default=False)

    class Meta:
        db_table = 'iceman_sources_products'
        ordering = ['source__name', 'order']
        verbose_name = 'Товар в магазине'
        verbose_name_plural = 'Товары в магазинах'
        unique_together = (('product', 'source'),)

    class OrderMeta:
        fk_fields = ('source', )

    def __str__(self):
        return self.product.name


class SourceProductPrice(models.Model):

    product = models.ForeignKey(SourceProduct, verbose_name='Товар', on_delete=models.CASCADE)
    price_type = models.CharField('Тип цены', max_length=255, db_index=True)
    price = models.FloatField('Цена')

    class Meta:
        db_table = 'iceman_sources_products_prices'
        ordering = ['product_id', 'price_type']
        verbose_name = 'Цена товара'
        verbose_name_plural = 'Цены товара'
        unique_together = (('product', 'price_type'), )

    def __str__(self):
        return f'Цена товара {self.product.product.name} типа {self.price_type}'


class ProductStock(models.Model):

    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, verbose_name='Склад', on_delete=models.CASCADE)
    count = models.IntegerField('Остаток', blank=True, null=True)

    class Meta:
        db_table = 'iceman_products_stocks'
        ordering = ['product_id', 'stock_id']
        verbose_name = 'Остаток товара на складе'
        verbose_name_plural = 'Остатки товаров на складе'
        unique_together = (('product', 'stock'), )

    def __str__(self):
        return f'Остаток товара {self.product.name} на складе {self.stock.name}'


class Order(models.Model):

    statuses = (
        (1, 'Новый'),
        (2, 'Просрочен'),
        (3, 'Оплачен'),
        (4, 'Отменен'),
        (5, 'Модерация'),
    )

    payment_types = (
        ('delay', 'Отсрочка'),
        ('fact', 'Факт'),
    )

    payment_methods = (
        ('entity', 'Юридическое лицо'),
        ('individual', 'Физическое лицо'),
    )

    email_statuses = (
        ('no_need', 'Не нужно'),
        ('wait', 'Ожидание'),
        ('sent', 'Отправлено'),
    )

    telegram_statuses = (
        ('no_need', 'Не нужно'),
        ('wait', 'Ожидание'),
        ('sent', 'Отправлено'),
    )

    te_statuses = (
        (1, _('Started')),
        (2, _('Finished')),
        (3, _('Checked')),
        (6, _('Pay in Solar')),
        (4, _('Payed')),
        (5, _('Denied')),
        (7, _('Not payed')),
        (8, _('Temp denied')),
    )

    date_create = models.DateTimeField('Дата заказа', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                             related_name='iceman_order_user')
    user_money = models.ForeignKey(User, verbose_name='Пользователь получения денег', on_delete=models.SET_NULL,
                                   null=True, related_name='iceman_order_user_money', blank=True)
    price = models.FloatField('Сумма', default=0, blank=True)

    delivery_date = models.DateField('Дата доставки')
    delivery_address = models.TextField('Адрес доставки', blank=True, default='')

    comment = models.TextField('Комментарий', default='', blank=True)

    store = models.ForeignKey(Store, verbose_name='Магазин', on_delete=models.SET_NULL, null=True, blank=True)
    task_id = models.IntegerField('Ид задачи', null=True, blank=True)
    task_status = models.IntegerField('Статус задачи', null=True, blank=True, choices=te_statuses)
    status = models.IntegerField('Статус', default=1, choices=statuses)

    payment_type = models.CharField('Тип оплаты', max_length=20, choices=payment_types, default='delay')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=payment_methods, default='individual')
    payment_status = models.BooleanField('Оплаченный', default=False)
    payment_sum_correct = models.FloatField('Реализация', default=0, blank=True)
    payment_sum = models.FloatField('Оплачено', default=0, blank=True)
    payment_phone = models.CharField('Телефон оплаты', max_length=20, null=True, blank=True)
    payment_days = models.IntegerField('Кол-во дней отсрочки', null=True, blank=True)
    payment_sum_user = models.FloatField('Бонус', default=0, blank=True)
    payment_courier = models.FloatField('Деньги водителю', null=True, blank=True)
    payment_url = models.CharField('Ссылка на оплату', max_length=1000, null=True, blank=True)

    price_type = models.CharField('Тип цены', max_length=255, null=True, blank=True)
    type = models.CharField('Тип заказа', max_length=20, choices=Store.types, null=True, blank=True)

    online_payment_id = models.CharField('Номер платежа', max_length=100, null=True, blank=True)
    online_payment_status = models.CharField('Статус платежа', max_length=100, null=True, blank=True)
    online_payment_sum = models.FloatField('Сумма платежа', blank=True, default=0)
    online_payment_url = models.CharField('Url платежа', max_length=1000, null=True, blank=True)
    online_payment_result = models.TextField('Результат платежа', null=True, blank=True)
    online_payment_qr_result = models.TextField('Результат запроса qr кода', null=True, blank=True)
    online_payment_qr = models.TextField('QR-код', null=True, blank=True)
    online_payment_qr_url = models.CharField('Url страницы с QR-кодом', max_length=1000, null=True, blank=True)
    online_payment_qr_file = models.ImageField('Изображение qr-кода', upload_to='iceman/qr/%Y/%m/%d/',
                                               null=True, blank=True)

    email_status = models.CharField('Статус отправки email', max_length=20, default='no_need', choices=email_statuses)
    telegram_status = models.CharField('Статус отправки telegram', max_length=20, default='no_need',
                                       choices=telegram_statuses)

    source = models.ForeignKey(Source, verbose_name='Источник', on_delete=models.SET_NULL, blank=True, null=True)

    sync_1c = models.BooleanField('Есть в 1с', null=True, blank=True)
    sync_1c_date = models.DateTimeField('Последняя синхронизация с 1с', blank=True, null=True)

    class Meta:
        db_table = 'iceman_orders'
        ordering = ['-date_create']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ # {self.id}'

    @property
    def products(self):
        return OrderProduct.objects.filter(order=self)

    @property
    def order_id(self):
        return f'ICM{self.id}'
    order_id.fget.short_description = 'Ид'

    @property
    def sum(self):
        if self.payment_sum_correct > 0:
            return self.payment_sum_correct
        return self.price

    @property
    def debt_sum(self):
        debt = round(self.payment_sum_correct - self.payment_sum, 2)
        if debt < 0:
            debt = 0
        return debt
    debt_sum.fget.short_description = 'Задолж.'

    @property
    def days_overdue(self):
        if self.is_payed:
            return None
        if self.payment_type != 'delay':
            return None
        if self.debt_sum <= 0:
            return None
        if self.status in [3, 4]:
            return None
        payment_days = 0 if self.payment_days is None else self.payment_days
        days = (date.today() - self.delivery_date - timedelta(days=payment_days)).days
        if days <= 0:
            return None
        return days
    days_overdue.fget.short_description = 'Просрочка'

    @property
    def is_payed(self):
        return self.payment_sum + 15 >= self.sum

    @property
    def user_sum(self):
        if self.source is None:
            return 0
        if self.payment_sum_correct > 0:
            curr_sum = self.payment_sum_correct
        else:
            curr_sum = self.sum
        if self.user and self.user.worker_bonus_iceman is not None:
            curr_user_sum = round(curr_sum * self.user.worker_bonus_iceman / 100, 2)
        else:
            curr_user_sum = round(curr_sum * self.source.worker_bonus / 100, 2)
        if self.user and self.user.status_legal != 'self_employed':
            curr_user_sum = round(curr_user_sum * 0.8, 2)
        return curr_user_sum


class OrderProduct(models.Model):

    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE,
                              related_name='iceman_order_product_order')

    code = models.CharField('Код', max_length=100)
    name = models.CharField('Название', max_length=200)
    brand_name = models.CharField('Производитель', max_length=200)
    unit = models.CharField('Ед. измерения', max_length=100)
    box_count = models.IntegerField('Кол-во в коробке', blank=True, default=1)

    count = models.IntegerField('Кол-во', default=1)

    price = models.FloatField('Цена', blank=True, default=0)
    price_one = models.FloatField('Цена за ед', blank=True, default=0)

    is_bonus = models.BooleanField('Бонусный товар', default=False)

    barcode = models.CharField('Штрихкод', max_length=15, default='')
    weight = models.IntegerField('Вес в граммах', null=True, blank=True)

    class Meta:
        db_table = 'iceman_order_products'
        ordering = ['-order_id', 'id']
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.name}'


class StoreTaskSchedule(models.Model):

    store = models.ForeignKey(Store, verbose_name='Магазин', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)

    per_week = models.IntegerField(_('How many times a week'), blank=True, null=True)
    per_month = models.IntegerField(_('How many times a month'), blank=True, null=True)
    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')
    is_once = models.BooleanField(_('Execution once'), default=False, blank=True)

    only_user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'iceman_stores_tasks_schedule'
        ordering = ['task__name', 'store__name', 'id']
        verbose_name = 'Расписание задачи в магазине'
        verbose_name_plural = 'Расписание задач'
        unique_together = (('store', 'task'), )

    def __str__(self):
        return f'Расписание задачи "{self.task}" в магазине "{self.store}"'


class StoreTask(models.Model):

    store = models.ForeignKey(Store, verbose_name='Магазин', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.SET_NULL, null=True, blank=True)

    only_user_id = models.IntegerField('Только для пользователя', null=True, blank=True)
    lock_user_id = models.IntegerField('Залочена для пользователя', null=True, blank=True)
    completed = models.BooleanField('Полностью выполнена', default=False)

    is_sync = models.BooleanField('Обновлено', default=False)

    update_time = models.DateTimeField('Время обновления', auto_now=True, null=True, blank=True)

    region = models.ForeignKey(Region,  verbose_name='Регион', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='iceman_store_task_region')

    days_of_week = models.CharField(_('Days of weeks'), max_length=100, blank=True, default='')
    done = models.BooleanField('Выполнена', default=False)

    class Meta:
        db_table = 'iceman_stores_tasks'
        ordering = ['store_id']
        verbose_name = 'Задача в магазине'
        verbose_name_plural = 'Задачи в магазинах сегодня'

    def __str__(self):
        if self.task:
            return f'{self.store} - {self.task}'
        else:
            return f'{self.store} - Продажа'
