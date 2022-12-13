from datetime import datetime
from django.conf import settings
from rest_framework import serializers, reverse, validators
from rest_framework.utils.serializer_helpers import BindingDict
from .models import User, Client, Region, Store, Good, Assortment, Task, TasksExecution, TasksExecutionImage, \
    Category, TasksExecutionAssortment, StoreTask, TasksExecutionAssortmentAll, TasksExecutionAssortmentBefore, Rank, \
    Act, TasksExecutionQuestionnaire, TasksExecutionOutReason, UserDevice, UserDeviceIceman
from application.inspector.models import InspectorGood


class UserDeviceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserDevice
        fields = (
            'id', 'date_create', 'date_use', 'name', 'os', 'version'
        )


class UserDeviceIcemanSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserDeviceIceman
        fields = (
            'id', 'date_create', 'date_use', 'name', 'os', 'version'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-user-detail', lookup_field='api_key')
    telegram = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    rank = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_agent = serializers.SerializerMethodField()
    status_iceman = serializers.SerializerMethodField()

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000

    class Meta:
        model = User
        fields = (
            'id', 'url', 'name', 'surname', 'phone', 'email', 'city', 'advisor', 'date_join', 'is_register',
            'is_banned', 'rank', 'status', 'status_agent', 'status_iceman', 'longitude', 'latitude', 'source',
            'telegram', 'api_key', 'status_legal', 'qlik_status', 'route'
        )

    @staticmethod
    def get_telegram(obj):
        return {
            'id': obj.telegram_id, 'language_code': obj.language_code,
            'last_name': obj.last_name, 'first_name': obj.first_name, 'username': obj.username
        }

    def get_rank_url(self, pk):
        return reverse.reverse('survey-api:rank-detail', args=[pk], request=self.context['request'])

    def get_rank(self, obj):
        if obj.rank:
            return {
                'id': obj.rank.id,
                'name': obj.rank.name,
                'url': self.get_rank_url(obj.rank.id)
            }
        else:
            return {

            }

    def get_status(self, obj):
        if obj.status:
            return {
                'id': obj.status.id,
                'name': obj.status.name,
            }
        else:
            return {

            }

    def get_status_agent(self, obj):
        if obj.status_agent:
            return {
                'id': obj.status_agent.id,
                'name': obj.status_agent.name,
            }
        else:
            return {

            }


    def get_status_iceman(self, obj):
        if obj.status_iceman:
            return {
                'id': obj.status_iceman.id,
                'name': obj.status_iceman.name,
                'default': obj.status_iceman.default,
            }
        else:
            return {

            }


    def __init__(self, *args, **kwargs):
        only_fields = kwargs.pop('only_fields', None)
        super().__init__(*args, **kwargs)

        if only_fields:
            fields = BindingDict(self)
            for key, value in self.get_fields().items():
                if key in only_fields:
                    fields[key] = value
            self.fields = fields


class UserFullSerializer(UserSerializer):

    devices = UserDeviceSerializer(source='user_device_user', many=True, read_only=True)
    devices_iceman = UserDeviceSerializer(source='user_device_iceman_user', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'name', 'surname', 'phone', 'email', 'city', 'advisor', 'date_join', 'is_register',
            'is_banned', 'rank', 'status', 'longitude', 'latitude', 'source', 'telegram', 'api_key', 'status_legal',
            'qlik_status', 'devices', 'devices_iceman'
        )


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='survey-api:client-detail')

    class Meta:
        model = Client
        fields = (
            'id', 'url', 'name'
        )


class RankSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='survey-api:rank-detail')

    class Meta:
        model = Rank
        fields = (
            'id', 'url', 'name', 'default', 'work_days', 'tasks_month', 'tasks_count', 'rate'
        )


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='survey-api:region-detail')

    class Meta:
        model = Region
        fields = (
            'id', 'url', 'name'
        )


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:store-detail')
    client = serializers.SerializerMethodField()
    region_o = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id', 'url', 'code', 'factory_code', 'address', 'longitude', 'latitude', 'auto_coord', 'days_of_week',
            'client', 'region_o', 'distance', 'category'
        )

    @staticmethod
    def get_distance(obj):
        try:
            return obj.distance
        except AttributeError:
            return None

    @staticmethod
    def get_category(obj):
        try:
            return obj.category.name
        except:
            return None

    def get_client_url(self, pk):
        return reverse.reverse('survey-api:client-detail', args=[pk], request=self.context['request'])

    def get_client(self, obj):
        return {
            'id': obj.client.id,
            'name': obj.client.name,
            'url': self.get_client_url(obj.client.id)
        }

    def get_region_url(self, pk):
        return reverse.reverse('survey-api:region-detail', args=[pk], request=self.context['request'])

    def get_region_o(self, obj):
        if obj.region_o:
            return {
                'id': obj.region_o.id,
                'name': obj.region_o.name,
                'url': self.get_region_url(obj.region_o.id)
            }
        else:
            return {
                'id': None,
                'name': obj.region,
                'url': None
            }


class InspectorGoodSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:inspector-good-detail')
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()

    class Meta:
        model = InspectorGood
        fields = (
            'id', 'url', 'name', 'cid', 'sku_id', 'category', 'brand', 'manufacturer'
        )

    @staticmethod
    def get_category(obj):
        try:
            return {
                'id': obj.category.id,
                'name': obj.category.name,
                'sku_id': obj.category.internal_id,
            }
        except:
            return {}

    @staticmethod
    def get_brand(obj):
        try:
            return {
                'id': obj.brand.id,
                'name': obj.brand.name,
                'sku_id': obj.brand.internal_id,
            }
        except:
            return {}

    @staticmethod
    def get_manufacturer(obj):
        try:
            return {
                'id': obj.manufacturer.id,
                'name': obj.manufacturer.name,
                'sku_id': obj.manufacturer.internal_id,
            }
        except:
            return {}


class GoodSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='survey-api:good-detail')

    class Meta:
        model = Good
        fields = (
            'id', 'url', 'name', 'image', 'description', 'code'
        )


class AssortmentSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:assortment-detail')
    store = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = Assortment
        fields = (
            'id', 'url', 'count', 'good', 'store', 'task'
        )

    def get_good_url(self, pk):
        return reverse.reverse('survey-api:good-detail', args=[pk], request=self.context['request'])

    def get_good(self, obj):
        return {
            'id': obj.good.id,
            'name': obj.good.name,
            'url': self.get_good_url(obj.good.id)
        }

    def get_store_url(self, pk):
        return reverse.reverse('survey-api:store-detail', args=[pk], request=self.context['request'])

    def get_store(self, obj):
        return {
            'id': obj.store.id,
            'code': obj.store.code,
            'factory_code': obj.store.factory_code,
            'url': self.get_store_url(obj.store.id)
        }

    def get_task_url(self, pk):
        return reverse.reverse('survey-api:task-detail', args=[pk], request=self.context['request'])

    def get_task(self, obj):
        if obj.task:
            return {
                'id': obj.task.id,
                'name': obj.task.name,
                'url': self.get_task_url(obj.task.id)
            }
        else:
            return {}


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:task-detail')
    customer = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'url', 'name', 'description', 'instruction', 'instruction_url', 'money', 'money_source', 'customer',
            'project'
        )

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TaskSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_project(self, obj):
        return obj.application

    def get_customer(self, obj):
        if obj.customer:
            return {
                'id': obj.customer.id,
                'name': obj.customer.name,
            }
        else:
            return {
                'id': None,
                'name': None,
            }


class TasksExecutionImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TasksExecutionImage
        fields = (
            'id', 'image', 'status', 'type', 'constructor_step_name'
        )


class TasksExecutionAssortmentSerializer(serializers.ModelSerializer):

    good = GoodSerializer(read_only=True)

    class Meta:
        model = TasksExecutionAssortment
        fields = (
            'good', 'avail', 'constructor_step_name'
        )


class TasksExecutionQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = TasksExecutionQuestionnaire
        fields = (
            'name', 'question', 'answer', 'constructor_step_name'
        )


class TasksExecutionBeforeSerializer(serializers.ModelSerializer):

    good = GoodSerializer(read_only=True)

    class Meta:
        model = TasksExecutionAssortmentBefore
        fields = (
            'good', 'avail',
        )


class TasksExecutionGoodSerializer(serializers.ModelSerializer):

    good = InspectorGoodSerializer(read_only=True)

    class Meta:
        model = TasksExecutionAssortmentAll
        fields = (
            'good', 'avail',
        )


class TasksExecutionOutReasonSerializer(serializers.ModelSerializer):

    good = GoodSerializer(read_only=True)
    out_reason = serializers.SerializerMethodField()

    class Meta:
        model = TasksExecutionOutReason
        fields = (
            'good', 'out_reason', 'image'
        )

    def get_out_reason(self, obj):
        return obj.out_reason.name


class TasksExecutionSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:task-execution-detail')
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    images = TasksExecutionImageSerializer(source='survey_tasksexecutionimage_task', many=True, read_only=True)
    avails = TasksExecutionAssortmentSerializer(source='survey_tasksexecutionassortment_task', many=True, read_only=True)
    goods = TasksExecutionGoodSerializer(source='tea_a_task', many=True, read_only=True)
    before = TasksExecutionBeforeSerializer(source='survey_tasksexecutionassortmentbefore_task', many=True, read_only=True)
    questionnaire = TasksExecutionQuestionnaireSerializer(source='survey_tasksexecutionquestionnaire_task', many=True, read_only=True)
    out_reasons = TasksExecutionOutReasonSerializer(source='survey_tasksexecutionoutreason_task', many=True, read_only=True)

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000

    class Meta:
        model = TasksExecution
        fields = (
            'id', 'url', 'date_start', 'date_end', 'status', 'money', 'money_source', 'user',
            'task', 'store', 'images', 'avails', 'goods', 'comments', 'before',
            'questionnaire', 'inspector_link', 'application', 'out_reasons'
        )

    def to_representation(self, instance):

        output_data = super().to_representation(instance)

        output_data['store'] = {}

        if instance.store:
            output_data['store']['id'] = instance.store.id
            output_data['store']['code'] = instance.store.code
            output_data['store']['factory_code'] = instance.store.factory_code
            output_data['store']['address'] = instance.store.address
            output_data['store']['longitude'] = instance.store.longitude
            output_data['store']['latitude'] = instance.store.latitude
            output_data['store']['client'] = instance.store.client.name
            output_data['store']['region'] = instance.store.region_o.name
            output_data['store']['category'] = instance.store.category.name
        elif instance.store_iceman:
            output_data['store']['id'] = 'ICMS' + str(instance.store_iceman.id) 
            output_data['store']['code'] = instance.store_iceman.code
            output_data['store']['factory_code'] = None
            output_data['store']['address'] = instance.store_iceman.address
            output_data['store']['longitude'] = instance.store_iceman.longitude
            output_data['store']['latitude'] = instance.store_iceman.latitude
            output_data['store']['client'] = instance.store_iceman.name
            output_data['store']['region'] = instance.store_iceman.region.name
            output_data['store']['category'] = instance.store_iceman.get_type_display()

        return output_data


class StoreTaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:store-task-detail')
    task = TaskSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    days = serializers.SerializerMethodField()

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000

    class Meta:
        model = StoreTask
        fields = (
            'id', 'url', 'task', 'store', 'per_week', 'per_month', 'days', 'is_once', 'hours_start', 'hours_end'
        )

    @staticmethod
    def get_days(obj):
        ar = []
        if not obj.days_of_week or '1' in obj.days_of_week:
            ar.append('понедельник')
        if not obj.days_of_week or '2' in obj.days_of_week:
            ar.append('вторник')
        if not obj.days_of_week or '3' in obj.days_of_week:
            ar.append('среда')
        if not obj.days_of_week or '4' in obj.days_of_week:
            ar.append('чертверг')
        if not obj.days_of_week or '5' in obj.days_of_week:
            ar.append('пятница')
        if not obj.days_of_week or '6' in obj.days_of_week:
            ar.append('суббота')
        if not obj.days_of_week or '7' in obj.days_of_week:
            ar.append('воскресенье')
        return ar


class PublicUserSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-user-detail', lookup_field='api_key')
    telegram = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    rank = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'url', 'name', 'surname', 'phone', 'email', 'city', 'advisor', 'date_join', 'is_register',
            'is_banned', 'rank', 'longitude', 'latitude', 'source', 'telegram', 'api_key'
        )

    @staticmethod
    def get_telegram(obj):
        return {
            'id': obj.telegram_id, 'language_code': obj.language_code,
            'last_name': obj.last_name, 'first_name': obj.first_name, 'username': obj.username
        }

    def get_rank_url(self, pk):
        return reverse.reverse('survey-api:rank-detail', args=[pk], request=self.context['request'])

    def get_rank(self, obj):
        if obj.rank:
            return {
                'id': obj.rank.id,
                'name': obj.rank.name,
                'url': self.get_rank_url(obj.rank.id)
            }
        else:
            return {

            }


class PublicClientSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-client-detail')

    class Meta:
        model = Client
        fields = (
            'id', 'url', 'name'
        )


class PublicCategorySerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-category-detail')

    class Meta:
        model = Category
        fields = (
            'id', 'url', 'name'
        )


class PublicRegionSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-region-detail')

    class Meta:
        model = Region
        fields = (
            'id', 'url', 'name'
        )


class PublicStoreSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-store-detail')
    client = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id', 'url', 'code', 'address', 'longitude', 'latitude', 'client', 'category', 'region', 'distance'
        )

    @staticmethod
    def get_distance(obj):
        try:
            return obj.distance
        except AttributeError:
            return None

    def get_client_url(self, pk):
        return reverse.reverse('survey-api:public-client-detail', args=[pk], request=self.context['request'])

    def get_client(self, obj):
        return {
            'id': obj.client.id,
            'name': obj.client.name,
            'url': self.get_client_url(obj.client.id)
        }

    def get_category(self, obj):
        if obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name,
                'url': self.get_category_url(obj)
            }
        else:
            return {
                'id': None,
                'name': None,
                'url': None
            }

    def get_region_url(self, pk):
        return reverse.reverse('survey-api:public-region-detail', args=[pk], request=self.context['request'])

    def get_category_url(self, obj):
        if obj:
            return reverse.reverse('survey-api:public-category-detail', args=[obj.category.id],
                                   request=self.context['request'])
        else:
            return None

    def get_region(self, obj):
        if obj.region_o:
            return {
                'id': obj.region_o.id,
                'name': obj.region_o.name,
                'url': self.get_region_url(obj.region_o.id)
            }
        else:
            return {
                'id': None,
                'name': obj.region,
                'url': None
            }


class PublicTaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:public-task-detail')

    class Meta:
        model = Task
        fields = (
            'id', 'url', 'name', 'description', 'instruction', 'instruction_url', 'money', 'money_source'
        )

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(PublicTaskSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)


class ActSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='survey-api:act-detail')
    user = UserSerializer(read_only=True, only_fields=['id', 'url', 'telegram_id'])
    image = serializers.SerializerMethodField()

    class Meta:
        model = Act
        fields = (
            'id', 'url', 'id_1c', 'number', 'date', 'date_update', 'user_fio', 'user_inn', 'user_phone', 'user_email',
            'sum', 'date_start', 'date_end', 'check_type', 'image', 'comment_manager', 'user',
        )

    def get_image(self, obj):
        return obj.url


class UsersTasksSerializer(serializers.ModelSerializer):

    sum = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'phone', 'name', 'surname', 'email', 'source', 'status_legal', 'qlik_status', 'sum', 'count', 'tasks'
        )

    def get_sum(self, obj):
        return round(obj.te_sum, 2)

    def get_count(self, obj):
        return obj.te_count

    def get_tasks(self, obj):

        items = TasksExecution.objects.filter(user=obj)

        if obj.filter_status and obj.filter_status != '':
            status = obj.filter_status.split(',')
            items = items.filter(status__in=status)

        if obj.filter_task and obj.filter_task != '':
            task = obj.filter_task.split(',')
            items = items.filter(task__id__in=task)

        if obj.filter_exclude_task and obj.filter_exclude_task != '':
            task = obj.filter_exclude_task.split(',')
            items = items.exclude(task__id__in=task)

        if obj.filter_date_start and obj.filter_date_start != '':
            dt = datetime.strptime(obj.filter_date_start, '%d.%m.%Y')
            items = items.filter(date_start__date__gte=dt.date())

        if obj.filter_date_end and obj.filter_date_end != '':
            dt = datetime.strptime(obj.filter_date_end, '%d.%m.%Y')
            items = items.filter(date_start__date__lte=dt.date())

        if obj.filter_date_start_e and obj.filter_date_start_e != '':
            dt = datetime.strptime(obj.filter_date_start_e, '%d.%m.%Y')
            items = items.filter(date_end__date__gte=dt.date())

        if obj.filter_date_end_e and obj.filter_date_end_e != '':
            dt = datetime.strptime(obj.filter_date_end_e, '%d.%m.%Y')
            items = items.filter(date_end__date__lte=dt.date())

        if obj.filter_organization and obj.filter_organization != '':
            items = items.filter(task__ss_account__name=obj.filter_organization)

        if obj.filter_project and obj.filter_project != '':
            items = items.filter(application=obj.filter_project)

        # items = items.values('task_id', 'task__name', 'task__customer__name', 'task__ss_account__name').annotate(
        #     count=Count('task_id'), sum=Sum('money')).values(
        #     'task_id', 'task__name', 'count', 'sum', 'task__customer__name', 'task__ss_account__name').order_by()

        items = items.values('task_id', 'task__name', 'task__customer__name', 'task__ss_account__name', 'application',
                             'money', 'store__address', 'store_iceman__address', 'date_start', 'date_end',
                             'store__code', 'store_iceman__code', 'store__longitude', 'store__latitude',
                             'store_iceman__longitude', 'store_iceman__latitude')

        data = []

        for i in items:

            project = None
            for app in settings.APPLICATIONS:
                if app[0] == i['application']:
                    project = app[1]

            if i['store__code']:
                location = {'longitude': i['store__longitude'], 'latitude': i['store__latitude']}
            else:
                location = {'longitude': i['store_iceman__longitude'], 'latitude': i['store_iceman__latitude']}

            data.append({
                'id': i['task_id'],
                'name': i['task__name'],
                'customer': i['task__customer__name'],
                'organization': i['task__ss_account__name'],
                'project': project,
                'sum': round(i['money'], 2),
                'address': i['store__address'] if (i['store__code']) else i['store_iceman__address'],
                'code': i['store__code'] if (i['store__code']) else i['store_iceman__code'],
                'location': location,
                'date_start': i['date_start'],
                'date_end': i['date_end'],
            })

        return data
