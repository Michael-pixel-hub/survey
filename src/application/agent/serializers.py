from rest_framework import serializers

from application.survey.serializers import UserSerializer

from .models import Store, Order, OrderGood, Payment, TinkoffPayment


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='agent-api:store-detail')
    user = UserSerializer(read_only=True)
    category = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    dadata = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    loyalty_program = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id', 'date_create', 'url', 'category', 'name', 'contact', 'phone', 'address', 'inn', 'agent',
            'price_type', 'is_agreement', 'loyalty_1c_code', 'loyalty_1c_user', 'loyalty_plan', 'loyalty_fact',
            'loyalty_cashback', 'loyalty_sumcashback', 'loyalty_cashback_payed', 'loyalty_cashback_to_pay',
            'loyalty_debt', 'loyalty_overdue_debt', 'loyalty_program', 'department', 'user', 'city', 'dadata',
        )

    @staticmethod
    def get_city(obj):
        try:
            return {
                'id': obj.city.id,
                'name': obj.city.name,
                'code': obj.city.code,
            }
        except:
            return {}

    @staticmethod
    def get_category(obj):
        if obj.category:
            return obj.category.name
        else:
            return None

    @staticmethod
    def get_dadata(obj):
        return {
            'name': obj.inn_name,
            'full_name': obj.inn_full_name,
            'director_title': obj.inn_director_title,
            'director_name': obj.inn_director_name,
            'address': obj.inn_address,
            'kpp': obj.inn_kpp,
            'ogrn': obj.inn_ogrn,
            'okved': obj.inn_okved,
        }

    @staticmethod
    def get_department(obj):

        if obj.loyalty_department:
            return {
                'name': obj.loyalty_department.name,
                'sys_name': obj.loyalty_department.sys_name,
            }
        else:
            return {
                'name': None,
                'sys_name': None,
            }

    @staticmethod
    def get_loyalty_program(obj):

        if obj.loyalty_program:
            return {
                'name': obj.loyalty_program.name,
                'sys_name': obj.loyalty_program.sys_name,
            }
        else:
            return {
                'name': None,
                'sys_name': None,
            }


class StoreOrderSerializer(StoreSerializer):

    class Meta:
        model = Store
        fields = (
            'id', 'date_create', 'url', 'category', 'name', 'contact', 'phone', 'address', 'inn', 'agent', 'price_type',
            'is_agreement', 'city', 'loyalty_1c_code', 'loyalty_1c_user', 'loyalty_plan', 'loyalty_fact',
            'loyalty_cashback', 'loyalty_sumcashback', 'loyalty_cashback_payed', 'loyalty_cashback_to_pay',
            'loyalty_debt', 'loyalty_overdue_debt', 'loyalty_program', 'department', 'dadata',
        )


class OrderGoodSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    class Meta:
        model = OrderGood
        fields = (
            'count', 'name', 'code', 'unit', 'price', 'sum', 'category', 'brand',
        )

    @staticmethod
    def get_category(obj):
        if obj.category:
            return {
                'name': obj.category.name,
            }
        else:
            return {}

    @staticmethod
    def get_brand(obj):
        if obj.brand:
            return {
                'name': obj.brand.name,
                'cashback_percent': obj.brand.cashback_percent,
            }
        else:
            return {}


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='agent-api:order-detail')
    user = UserSerializer(read_only=True)
    store = StoreOrderSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    from_1c_data = serializers.SerializerMethodField()
    goods = OrderGoodSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'date_order', 'url', 'delivery_address', 'delivery_date', 'sum', 'cashback_sum', 'comment',
            'comments_status', 'status', 'need_check', 'store', 'user', 'from_1c_data', 'payment', 'goods',
        )

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()

    @staticmethod
    def get_from_1c_data(obj):
        return {
            'firm': obj.from_1c_firm,
            'sum': obj.from_1c_sum,
            'pay': obj.from_1c_pay,
            'status': obj.from_1c_status,
        }

    @staticmethod
    def get_payment(obj):
        return {
            'type': obj.payment_type,
            'status': obj.payment_status,
            'sum': obj.payment_sum,
        }


class PaymentSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='agent-api:payment-detail')

    class Meta:
        model = Payment
        fields = (
            'id', 'url', 'date_create', 'source', 'provider', 'currency', 'total_amount', 'invoice_payload',
            'telegram_payment_charge_id', 'provider_payment_charge_id'
        )


class TinkoffPaymentSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='agent-api:tinkoff-payment-detail')

    class Meta:
        model = TinkoffPayment
        fields = (
            'id', 'url', 'terminal_key', 'order_id', 'success', 'status', 'payment_id', 'error_code', 'amount', 'card_id',
            'pan', 'exp_date'
        )
