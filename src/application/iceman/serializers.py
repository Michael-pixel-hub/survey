from application.survey.serializers import UserSerializer
from application.survey.models import User
from rest_framework import serializers


from .models import Store, StoreDocument, StoreStock, Order, OrderProduct


class IcemanUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'url', 'name', 'surname', 'phone', 'email', 'city', 'advisor', 'date_join', 'is_register',
            'is_banned', 'longitude', 'latitude', 'source', 'status_legal', 'qlik_status', 'status_iceman'
        )


class StoreDocumentSerializer(serializers.ModelSerializer):

    file = serializers.SerializerMethodField()

    class Meta:
        model = StoreDocument
        fields = (
            'type', 'number', 'file'
        )

    def get_file(self, obj):
        request = self.context.get('request')
        file_url = obj.file.url
        return request.build_absolute_uri(file_url)


class StoreStockSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    sys_name = serializers.SerializerMethodField()

    class Meta:
        model = StoreStock
        fields = (
            'name', 'sys_name'
        )

    @staticmethod
    def get_name(obj):
        return obj.stock.name

    @staticmethod
    def get_sys_name(obj):
        return obj.stock.sys_name


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='iceman-api:store-detail')
    region = serializers.SerializerMethodField()
    dadata = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    stocks = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id', 'url', 'type', 'name', 'code', 'region', 'address', 'longitude', 'latitude', 'inn', 'dadata',
            'is_agreement', 'is_agreement_data', 'is_order_task', 'is_entry', 'lpr_phone', 'lpr_fio', 'director_phone',
            'director_fio', 'price_type', 'photo', 'schedule', 'payment_days', 'sum_restrict', 'source', 'documents',
            'stocks'
        )

    @staticmethod
    def get_region(obj):
        if obj.region:
            return {
                'id': obj.region.id,
                'name': obj.region.name,
                'short_name': obj.region.short_name,
                'short_name_2': obj.region.short_name_2,
                'name_1c': obj.region.name_1c,
                'name_1c_2': obj.region.name_1c_2,
            }
        else:
            return {}

    @staticmethod
    def get_dadata(obj):
        return {
            'name': obj.inn_name,
            'full_name': obj.inn_name_1,
            'director_title': obj.inn_director_title,
            'director_name': obj.inn_director_name,
            'address': obj.inn_address,
            'kpp': obj.inn_kpp,
            'ogrn': obj.inn_ogrn,
            'okved': obj.inn_okved,
            'type': obj.inn_type,
            'region': obj.inn_region,
        }

    def get_documents(self, obj):
        request = self.context.get('request')
        items = StoreDocumentSerializer(obj.iceman_store_document_store.all(), many=True, context={'request': request})
        return items.data

    def get_stocks(self, obj):
        request = self.context.get('request')
        items = StoreStockSerializer(obj.iceman_store_stock_store.all(), many=True, context={'request': request})
        return items.data

    @staticmethod
    def get_source(obj):
        if obj.source:
            return {
                'id': obj.source.id,
                'name': obj.source.name,
                'sys_name': obj.source.sys_name,
                'partner_name': obj.source.partner_name,
                'partner_email': obj.source.partner_email,
                'partner_fio': obj.source.partner_fio,
                'partner_phone': obj.source.partner_phone,
                'bonus': obj.source.bonus,
                'discount': obj.source.discount,
                'sum_restrict': obj.source.sum_restrict,
                'delivery_max_days': obj.source.delivery_max_days,
                'worker_bonus': obj.source.worker_bonus,
                'payment_days': obj.source.payment_days,
            }
        else:
            return {}

    @staticmethod
    def get_id(obj):
        return obj.store_id


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = (
            'code', 'name', 'brand_name', 'unit', 'box_count', 'count', 'price', 'price_one', 'is_bonus', 'barcode',
            'weight'
        )


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='iceman-api:order-detail')
    user = IcemanUserSerializer(read_only=True)
    user_money = IcemanUserSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    products = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'url', 'date_create', 'user', 'user_money', 'price', 'delivery_date', 'delivery_address', 'comment',
            'source', 'store', 'task_id', 'status', 'payment_type', 'payment_method', 'payment_status', 'payment_sum',
            'payment_sum_correct', 'payment_days', 'payment_sum_user', 'payment_phone', 'payment_courier',
            'payment_url', 'price_type', 'type', 'debt_sum', 'days_overdue', 'online_payment_id',
            'online_payment_status', 'online_payment_sum', 'online_payment_url', 'online_payment_result',
            'online_payment_qr_result', 'online_payment_qr', 'online_payment_qr_url', 'online_payment_qr_file',
            'products'
        )

    @staticmethod
    def get_id(obj):
        return obj.order_id

    def get_products(self, obj):
        request = self.context.get('request')
        items = OrderProductSerializer(obj.iceman_order_product_order.all(), many=True, context={'request': request})
        return items.data

    @staticmethod
    def get_source(obj):
        if obj.source:
            return {
                'id': obj.source.id,
                'name': obj.source.name,
                'sys_name': obj.source.sys_name,
                'partner_name': obj.source.partner_name,
                'partner_email': obj.source.partner_email,
                'partner_fio': obj.source.partner_fio,
                'partner_phone': obj.source.partner_phone,
                'bonus': obj.source.bonus,
                'discount': obj.source.discount,
                'sum_restrict': obj.source.sum_restrict,
                'delivery_max_days': obj.source.delivery_max_days,
                'worker_bonus': obj.source.worker_bonus,
                'payment_days': obj.source.payment_days,
            }
        else:
            return {}
