from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.fields import Field

from .models import Order, Store, PromoCode


class OrderResource(resources.ModelResource):

    user__name = Field(attribute='user__name', column_name=_('User name'))
    user__surname = Field(attribute='user__surname', column_name=_('User surname'))
    user__email = Field(attribute='user__email', column_name=_('User email'))
    store_name = Field(attribute='store__name', column_name=_('Store name'))
    store_address = Field(attribute='store__address', column_name=_('Store address'))
    store_inn = Field(attribute='store__inn', column_name=_('Store inn'))
    store_city = Field(attribute='store__city__name', column_name=_('Store city'))
    status = Field(attribute='get_status_display', column_name=_('Status'))
    from_1c_firm = Field(attribute='from_1c_firm', column_name=_('Payment firm'))
    from_1c_sum = Field(attribute='from_1c_sum', column_name=_('1c sum'))
    from_1c_pay = Field(attribute='from_1c_pay', column_name=_('1c pay sum'))
    from_1c_status = Field(attribute='from_1c_status', column_name=_('1c status'))

    class Meta:
        model = Order
        fields = ('id', 'date_order', 'user__name', 'user__surname', 'user__email', 'store_name', 'store_address',
                  'store_inn', 'store_city', 'comment', 'delivery_address', 'delivery_date', 'sum', 'cashback_sum',
                  'status', 'comments_status', 'from_1c_firm', 'from_1c_sum', 'from_1c_pay', 'from_1c_status')
        export_order = (
            'id', 'date_order', 'user__name', 'user__surname', 'user__email', 'store_name', 'store_address',
                  'store_inn', 'store_city', 'comment', 'delivery_address', 'delivery_date', 'sum', 'cashback_sum',
            'status', 'comments_status', 'from_1c_firm', 'from_1c_sum', 'from_1c_pay', 'from_1c_status')


class StoreResource(resources.ModelResource):

    date_create = Field(attribute='date_create', column_name=_('Date create'))
    name = Field(attribute='name', column_name=_('Name'))
    contact = Field(attribute='contact', column_name=_('Contact face'))
    phone = Field(attribute='phone', column_name=_('Phone'))
    address = Field(attribute='address', column_name=_('Address'))
    inn = Field(attribute='inn', column_name=_('Inn'))
    city = Field(attribute='city__name', column_name=_('City'))
    city_code = Field(attribute='city__code', column_name=_('City code'))
    user_id = Field(attribute='user__id', column_name=_('User id'))
    user_name = Field(attribute='user__name', column_name=_('User name'))
    user_surname = Field(attribute='user__surname', column_name=_('User surname'))
    user_email = Field(attribute='user__email', column_name=_('User email'))
    user_advisor = Field(attribute='user__advisor', column_name=_('Advisor'))
    user_phone = Field(attribute='user__phone', column_name=_('User phone'))
    last_order_id = Field(attribute='last_order_id', column_name=_('Last order id'))
    last_order_date = Field(attribute='last_order_date', column_name=_('Last order date'))

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset and queryset.extra(
            select={
                'last_order_id': '(SELECT "agent_orders".id FROM "agent_orders" '
                                 'WHERE "agent_stores"."id" = "agent_orders".store_id '
                                 'ORDER BY "agent_orders".date_order DESC LIMIT 1)',
                'last_order_date': '(SELECT "agent_orders".date_order FROM "agent_orders" '
                                   'WHERE "agent_stores"."id" = "agent_orders".store_id '
                                   'ORDER BY "agent_orders".date_order DESC LIMIT 1)'
            }
        ).prefetch_related('user')
        return super(StoreResource, self).export(queryset, *args, **kwargs)

    class Meta:
        model = Store
        fields = ('id', 'date_create', 'name', 'contact', 'phone', 'address', 'inn', 'city', 'city_code', 'user_id',
                  'user_name', 'user_surname', 'user_email', 'user_phone', 'user_advisor', 'last_order_id',
                  'last_order_date')
        export_order = ('id', 'date_create', 'name', 'contact', 'phone', 'address', 'inn', 'city', 'city_code',
                        'user_name', 'user_surname', 'user_email', 'user_advisor', 'last_order_id', 'last_order_date',
                        'user_id', 'user_phone')


class PromoCodeResource(resources.ModelResource):

    class Meta:
        model = PromoCode
        import_id_fields = ('code',)
        exclude = ('id',)
        skip_unchanged = True
        fields = ('code',)


class StoreImportResource(resources.ModelResource):

    id = Field(attribute='id', column_name='Ид')
    loyalty_plan = Field(attribute='loyalty_plan', column_name='План')
    loyalty_fact = Field(attribute='loyalty_fact', column_name='Факт')
    loyalty_sumcashback = Field(attribute='loyalty_sumcashback', column_name='Кэш-бэк заработан')
    loyalty_cashback_payed = Field(attribute='loyalty_cashback_payed', column_name='Кэш-бэк выплачен')
    loyalty_cashback_to_pay = Field(attribute='loyalty_cashback_to_pay', column_name='Кэш-бэк к выплате')

    def init_instance(self, row=None):
        import datetime
        instance = super().init_instance(row)
        instance.date_create = datetime.datetime.now()
        instance.user_id = 2
        return instance

    def before_import_row(self, row, row_number=None, **kwargs):
        try:
            if row.get('План'):
                row['План'] = row['План'].replace(',', '.')
        except:
            pass
        if row.get('План') == '':
            row['План'] = 0
        try:
            if row.get('Факт'):
                row['Факт'] = row['Факт'].replace(',', '.')
        except:
            pass
        if row.get('Факт') == '':
            row['Факт'] = 0
        try:
            if row.get('Кэш-бэк заработан'):
                row['Кэш-бэк заработан'] = row['Кэш-бэк заработан'].replace(',', '.')
        except:
            pass
        if row.get('Кэш-бэк заработан') == '':
            row['Кэш-бэк заработан'] = 0
        try:
            if row.get('Кэш-бэк выплачен'):
                row['Кэш-бэк выплачен'] = row['Кэш-бэк выплачен'].replace(',', '.')
        except:
            pass
        if row.get('Кэш-бэк выплачен') == '':
            row['Кэш-бэк выплачен'] = 0
        try:
            if row.get('Кэш-бэк к выплате'):
                row['Кэш-бэк к выплате'] = row['Кэш-бэк к выплате'].replace(',', '.')
        except:
            pass
        if row.get('Кэш-бэк к выплате') == '':
            row['Кэш-бэк к выплате'] = 0


    class Meta:
        model = Store
        import_id_fields = ('id', )
        #skip_unchanged = True
        fields = ('id', 'loyalty_plan', 'loyalty_fact', 'loyalty_sumcashback', 'loyalty_cashback_payed', 'loyalty_cashback_to_pay', )
        import_order = ('id', 'loyalty_plan', 'loyalty_fact', 'loyalty_sumcashback', 'loyalty_cashback_payed', 'loyalty_cashback_to_pay',)
        exclude = ('id',)
