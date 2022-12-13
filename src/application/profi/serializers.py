from rest_framework import serializers

from application.survey.models import Store, Client, Region
from application.survey.serializers import ClientSerializer, StoreSerializer, RegionSerializer

from .models import String, User, Menu, Report, Task, Order


class StringSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:string-detail', lookup_field='slug')

    class Meta:
        model = String
        fields = (
            'slug', 'url', 'name', 'category', 'value'
        )


class MenuSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:menu-detail')

    class Meta:
        model = Menu
        fields = (
            'id', 'url', 'name', 'value'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:user-detail')
    telegram = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'date_join', 'is_register', 'company_name', 'company_inn', 'fio', 'phone', 'email', 'telegram',
            'is_telegram', 'telegram_id', 'telegram_language_code', 'telegram_last_name', 'telegram_first_name',
            'telegram_username'
        )
        extra_kwargs = {
            'is_telegram': {'write_only': True},
            'telegram_id': {'write_only': True},
            'telegram_language_code': {'write_only': True},
            'telegram_last_name': {'write_only': True},
            'telegram_first_name': {'write_only': True},
            'telegram_username': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields:
            s_fields = []
            for i in self.fields:
                s_fields.append(str(i))
            for i in s_fields:
                if i not in fields:
                    self.fields.pop(i)

    @staticmethod
    def get_telegram(obj):
        return {
            'is_telegram': obj.is_telegram, 'id': obj.telegram_id, 'language_code': obj.telegram_language_code,
            'last_name': obj.telegram_last_name, 'first_name': obj.telegram_first_name,
            'username': obj.telegram_username
        }


class ReportSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:report-detail')
    user = UserSerializer(read_only=True, fields=('id', 'url'))

    class Meta:
        model = Report
        fields = (
            'id', 'url', 'file', 'description', 'user'
        )


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:task-detail')
    author = UserSerializer(read_only=True, fields=('id', 'url'))
    author_id = serializers.PrimaryKeyRelatedField(source='author', queryset=User.objects.filter(is_register=True),
                                                   write_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'url', 'type', 'name', 'description', 'price', 'is_offered', 'author', 'date_offered', 'author_id'
        )


class Calc(object):

    def __init__(self, *args, **kwargs):

        self.task = kwargs.get('task')
        self.stores = kwargs.get('stores')
        self.regions = kwargs.get('regions')
        self.clients = kwargs.get('clients')

    def calc(self):

        price = 0

        # Task
        if self.task:
            try:
                task = Task.objects.get(id=self.task)
                price = task.price
            except (Task.DoesNotExist, ValueError):
                pass

        # Stores
        stores = []
        if self.stores:
            try:
                stores_data = self.stores.split(',')
                ids = Store.objects.filter(id__in=stores_data).values_list('id', flat=True)
                stores += list(ids)
            except ValueError:
                pass

        # Clients
        if self.clients:
            try:
                clients_data = self.clients.split(',')
                ids = Store.objects.filter(client__in=clients_data).values_list('id', flat=True)
                stores += list(ids)
            except ValueError:
                pass

        # Regions
        if self.regions:
            try:
                regions_data = self.regions.split(',')
                ids = Store.objects.filter(region_o__in=regions_data).values_list('id', flat=True)
                stores += list(ids)
            except ValueError:
                pass

        stores_count = len(list(set(stores)))

        result = [
            {
                'value': price * stores_count,
                'price': price,
                'stores_count': stores_count
            }
        ]
        return result


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='profi-api:order-detail')
    user = UserSerializer(required=False)
    task = TaskSerializer(required=False)
    clients_list = ClientSerializer(source='clients', read_only=True, many=True)
    stores_list = StoreSerializer(source='stores', read_only=True, many=True)
    regions_list = RegionSerializer(source='regions', read_only=True, many=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.filter(is_register=True),
                                                 write_only=True)
    task_id = serializers.PrimaryKeyRelatedField(source='task', queryset=Task.objects.filter(is_public=True),
                                                 write_only=True)
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'url', 'date_start', 'date_end', 'status', 'status_text', 'date_create', 'date_finish',
            'user', 'task', 'clients_list', 'stores_list', 'regions_list', 'user_id', 'task_id', 'per_week',
            'days_of_week', 'is_once'
        )

    def create(self, validated_data):

        obj = super().create(validated_data)

        clients = self.initial_data.get('clients')
        if clients:
            clients_list = Client.objects.filter(id__in=clients)
            obj.clients.set(clients_list)
            obj.save()

        regions = self.initial_data.get('regions')
        if regions:
            regions_list = Region.objects.filter(id__in=regions)
            obj.regions.set(regions_list)
            obj.save()

        stores = self.initial_data.get('stores')
        if stores:
            stores_list = Store.objects.filter(id__in=stores)
            obj.stores.set(stores_list)
            obj.save()

        return obj

    @staticmethod
    def get_status_text(obj):
        return obj.get_status_display()
