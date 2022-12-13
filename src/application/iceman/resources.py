from import_export import resources
from import_export.fields import Field
from import_export.widgets import NumberWidget, DateTimeWidget, DateWidget

from .models import Order


class OrderResource(resources.ModelResource):

    id = Field(attribute='order_id', column_name='Ид')
    date_create = Field(attribute='date_create', column_name='Дата заказа', widget=DateTimeWidget())
    delivery_date = Field(attribute='delivery_date', column_name='Дата доставки', widget=DateWidget())
    user_name = Field(attribute='user__name', column_name='ФИО пользователя')
    user_email = Field(attribute='user__email', column_name='E-mail пользователя')
    user_status = Field(column_name='Статус пользователя')
    user_region = Field(column_name='Регион пользователя')
    store_name = Field(column_name='Магазин')
    delivery_address = Field(attribute='delivery_address', column_name='Адрес')
    payment_type = Field(attribute='payment_type', column_name='Тип оплаты')
    price = Field(attribute='price', column_name='Сумма заказа', widget=NumberWidget())
    payment_sum_correct = Field(attribute='payment_sum_correct', column_name='Сумма реализации', widget=NumberWidget())
    payment_sum = Field(attribute='payment_sum', column_name='Сумма оплаты', widget=NumberWidget())
    debt_sum = Field(attribute='debt_sum', column_name='Задолженность', widget=NumberWidget())
    days_overdue = Field(attribute='days_overdue', column_name='Просрочка')
    payment_sum_user = Field(attribute='payment_sum_user', column_name='Бонус пользователю', widget=NumberWidget())
    task_status = Field(attribute='task_status', column_name='Статус задачи')
    status = Field(attribute='status', column_name='Статус')
    sync_1c = Field(attribute='sync_1c', column_name='Есть в 1с')
    sync_1c_date = Field(attribute='sync_1c_date', column_name='Дата синхронизации')

    class Meta:
        model = Order
        fields = ('id', 'date_create', 'delivery_date', 'user_name', 'user_email', 'user_status', 'user_region'
                  , 'store_name', 'delivery_address' 'payment_type', 'price', 'payment_sum_correct', 'payment_sum',
                  'debt_sum', 'days_overdue', 'payment_sum_user', 'task_status', 'status', 'sync_1c', 'sync_1c_date')

    def dehydrate_user_status(self, obj):
        if obj.user is None:
            return '-'
        return obj.user.get_status_legal_display()

    def dehydrate_user_name(self, obj):
        if obj.user is None:
            return '-'
        return f'{obj.user.surname} {obj.user.name}'

    def dehydrate_store_name(self, obj):
        if obj.store is None:
            return '-'
        return str(obj.store)

    def dehydrate_user_region(self, obj):
        if obj.user is None:
            return '-'
        return obj.user.city

    def dehydrate_task_status(self, obj):
        if obj.task_status is None:
            return '-'
        return str(obj.get_task_status_display())

    def dehydrate_status(self, obj):
        return str(obj.get_status_display())

    def dehydrate_payment_type(self, obj):
        return str(obj.get_payment_type_display())

    def dehydrate_sync_1c(self, obj):
        if obj.sync_1c is None:
            return '-'
        return 'Да' if obj.sync_1c else 'Нет'
