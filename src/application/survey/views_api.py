import datetime

from django.conf import settings
from django.db.models import Q, Exists, OuterRef, Sum, Subquery, FloatField, Count, IntegerField, Value, CharField

from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from preferences.utils import get_setting

from .models import User, Client, Region, Store, Good, Assortment, Task, TasksExecution, Category, StoreTask, Rank, Act
from application.inspector.models import InspectorGood
from .serializers import UserSerializer, ClientSerializer, RegionSerializer, StoreSerializer, GoodSerializer, \
    AssortmentSerializer, TaskSerializer, TasksExecutionSerializer, PublicUserSerializer, PublicClientSerializer, \
    PublicCategorySerializer, PublicRegionSerializer, PublicStoreSerializer, StoreTaskSerializer, \
    InspectorGoodSerializer, RankSerializer, ActSerializer, UsersTasksSerializer, UserFullSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'Users': reverse('survey-api:user-list', request=request),
        'Ranks': reverse('survey-api:rank-list', request=request),
        'Clients': reverse('survey-api:client-list', request=request),
        'Regions': reverse('survey-api:region-list', request=request),
        'Stores': reverse('survey-api:store-list', request=request),
        'Goods': reverse('survey-api:good-list', request=request),
        'Inspector goods': reverse('survey-api:inspector-good-list', request=request),
        'Assortments': reverse('survey-api:assortment-list', request=request),
        'Tasks': reverse('survey-api:task-list', request=request),
        'Tasks executions': reverse('survey-api:task-execution-list', request=request),
        'Store tasks': reverse('survey-api:store-task-list', request=request),
        'Acts': reverse('survey-api:act-list', request=request),
        'Users tasks': reverse('survey-api:users-tasks', request=request),
        #'Public user': reverse('survey-api:public-user', request=request),
        'Public clients': reverse('survey-api:public-client-list', request=request),
        'Public categories': reverse('survey-api:public-category-list', request=request),
        'Public region': reverse('survey-api:public-region-list', request=request),
        'Public stores': reverse('survey-api:public-store-list', request=request),
    })


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):

        q = User.objects.all().select_related('rank', 'status', 'status_agent', 'status_iceman')
        if self.request.GET.get('date'):
            dt = datetime.datetime.strptime(self.request.GET.get('date'), '%d.%m.%Y')
            q = q.filter(date_join__date=dt.date())

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ClientListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = ClientSerializer

    def get_queryset(self):

        q = Client.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClientDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Client.objects.filter(is_public=True)
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RankListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = RankSerializer

    def get_queryset(self):

        q = Rank.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RankDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Rank.objects.filter(is_public=True)
    serializer_class = RankSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RegionListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = RegionSerializer

    def get_queryset(self):

        q = Region.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegionDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Region.objects.filter(is_public=True)
    serializer_class = RegionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StoreListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = StoreSerializer

    def get_queryset(self):

        q = Store.objects.filter(is_public=True).prefetch_related('client', 'category').prefetch_related('region_o')

        if self.kwargs.get('longitude') and self.kwargs.get('latitude'):

            q = q.extra(
                select={
                    'distance': 'ST_Distance(ST_Point(longitude, latitude)::geography, ST_Point(%s, %s)::geography) '
                                '/ 1000' % (self.kwargs.get('longitude'), self.kwargs.get('latitude'))
                },
                where=[
                    'ST_Distance(ST_Point(longitude, latitude)::geography, ST_Point(%s, %s)::geography) / 1000 < %s'
                    % (self.kwargs.get('longitude'), self.kwargs.get('latitude'),
                       get_setting('survey_storesearchradius'))
                ]

            )
            q = q.order_by('distance')

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StoreDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Store.objects.filter(is_public=True)
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GoodListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Good.objects.filter(is_public=True)
    serializer_class = GoodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoodDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Good.objects.filter(is_public=True)
    serializer_class = GoodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class InspectorGoodListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = InspectorGood.objects.all().prefetch_related('category', 'brand', 'manufacturer')
    serializer_class = InspectorGoodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InspectorGoodDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = InspectorGood.objects.all()
    serializer_class = InspectorGoodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# class InspectorBeforeListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = InspectorGood.objects.all()
#     serializer_class = InspectorBeforeSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#
# class InspectorBeforeDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = InspectorGood.objects.all()
#     serializer_class = InspectorBeforeSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class AssortmentListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Assortment.objects.filter(is_public=True).prefetch_related('store').prefetch_related('good')
    serializer_class = AssortmentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AssortmentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Assortment.objects.filter(is_public=True)
    serializer_class = AssortmentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TaskListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Task.objects.filter(is_public=True).prefetch_related('clients').prefetch_related('regions').\
        prefetch_related('stores', 'customer').prefetch_related('stores__client').prefetch_related('stores__region_o')
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TaskDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Task.objects.filter(is_public=True)
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TasksExecutionListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = TasksExecutionSerializer

    def get_queryset(self):

        q = TasksExecution.objects.all().prefetch_related(
            'task', 'task__customer', 'user', 'user__rank', 'store', 'store_iceman',
            'store__client', 'store__region_o', 'store_iceman__region', 'survey_tasksexecutionimage_task',
            'tea_a_task', 'tea_a_task__good', 'tea_a_task__good__category',
            'tea_a_task__good__manufacturer', 'tea_a_task__good__brand',
            'survey_tasksexecutionassortment_task', 'survey_tasksexecutionassortment_task__good',
            'survey_tasksexecutionassortmentbefore_task', 'survey_tasksexecutionassortmentbefore_task__good',
            'survey_tasksexecutionoutreason_task', 'survey_tasksexecutionquestionnaire_task',
            'survey_tasksexecutionoutreason_task__out_reason', 'survey_tasksexecutionoutreason_task__good',
            'store__category', 'user__status', 'user__status_agent', 'user__status_iceman'
        )
        if self.request.GET.get('date'):
            dt = datetime.datetime.strptime(self.request.GET.get('date'), '%d.%m.%Y')
            q = q.filter(date_start__date=dt.date())
        if self.request.GET.get('date_start_gt'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_start_gt'), '%d.%m.%Y %H:%M')
            q = q.filter(date_start__gte=dt)
        if self.request.GET.get('date_start_lt'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_start_lt'), '%d.%m.%Y %H:%M')
            q = q.filter(date_start__lte=dt)
        if self.request.GET.get('status'):
            q = q.filter(status__in=self.request.GET.getlist('status'))
        if self.request.GET.get('phone'):
            q = q.filter(user__phone=self.request.GET.get('phone'))
        if self.request.GET.get('email'):
            q = q.filter(user__email=self.request.GET.get('email'))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TasksExecutionDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = TasksExecution.objects.all()
    serializer_class = TasksExecutionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StoreTaskListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = StoreTaskSerializer

    def get_queryset(self):

        q = StoreTask.objects.all().prefetch_related(
            'task', 'store', 'store__category', 'store__client', 'store__category', 'store__region_o')
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StoreTaskDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = StoreTask.objects.all()
    serializer_class = StoreTaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PublicUserCreateView(mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = PublicUserSerializer

    permission_classes = ()
    authentication_classes = ()
    lookup_field = 'api_key'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PublicUserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView, mixins.UpdateModelMixin):

    queryset = User.objects.all()
    serializer_class = PublicUserSerializer

    permission_classes = ()
    authentication_classes = ()
    lookup_field = 'api_key'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PublicClientListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PublicClientSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):

        q = Client.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PublicClientDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Client.objects.filter(is_public=True)
    serializer_class = PublicClientSerializer
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PublicCategoryListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PublicCategorySerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):

        q = Category.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PublicCategoryDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Category.objects.filter(is_public=True)
    serializer_class = PublicCategorySerializer
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PublicRegionListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PublicRegionSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):

        q = Region.objects.filter(is_public=True)
        if self.kwargs.get('search'):
            search_q = self.kwargs.get('search')
            q = q.filter(Q(name__search=search_q) | Q(name__icontains=search_q))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PublicRegionDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Region.objects.filter(is_public=True)
    serializer_class = PublicRegionSerializer
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PublicStoreListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PublicStoreSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):

        q = Store.objects.filter(is_public=True).prefetch_related('client').prefetch_related('region_o').\
            prefetch_related('category')

        if self.kwargs.get('longitude') and self.kwargs.get('latitude'):

            q = q.extra(
                select={
                    'distance': 'ST_Distance(ST_Point(longitude, latitude)::geography, ST_Point(%s, %s)::geography) '
                                '/ 1000' % (self.kwargs.get('longitude'), self.kwargs.get('latitude'))
                },
                where=[
                    'ST_Distance(ST_Point(longitude, latitude)::geography, ST_Point(%s, %s)::geography) / 1000 < %s'
                    % (self.kwargs.get('longitude'), self.kwargs.get('latitude'),
                       get_setting('survey_storesearchradius'))
                ]

            )
            q = q.order_by('distance')

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PublicStoreDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Store.objects.filter(is_public=True)
    serializer_class = PublicStoreSerializer
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ActListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Act.objects.filter(check_type__in=['true'], url__isnull=False).select_related('user', 'user__rank').\
        order_by('-date_update')
    serializer_class = ActSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ActDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Act.objects.all().select_related('user', 'user__rank').order_by('-date_update')
    serializer_class = ActSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UsersTasksListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UsersTasksSerializer

    def get_queryset(self):

        te = TasksExecution.objects.filter(user=OuterRef('pk'))
        sum_te = te.values('user_id').annotate(sm=Sum('money')).values('sm').order_by()
        count_te = te.values('user_id').annotate(c=Count('id')).values('c').order_by()

        if self.request.GET.get('status'):
            status = str(self.request.GET.get('status')).split(',')
            te = te.filter(status__in=status)
            sum_te = sum_te.filter(status__in=status)
            count_te = count_te.filter(status__in=status)

        if self.request.GET.get('task'):
            task = str(self.request.GET.get('task')).split(',')
            te = te.filter(task_id__in=task)
            sum_te = sum_te.filter(task_id__in=task)
            count_te = count_te.filter(task_id__in=task)

        if self.request.GET.get('exclude_task'):
            task = str(self.request.GET.get('exclude_task')).split(',')
            te = te.exclude(task_id__in=task)
            sum_te = sum_te.exclude(task_id__in=task)
            count_te = count_te.exclude(task_id__in=task)

        if self.request.GET.get('date_start'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_start'), '%d.%m.%Y')
            te = te.filter(date_start__date__gte=dt.date())
            sum_te = sum_te.filter(date_start__date__gte=dt.date())
            count_te = count_te.filter(date_start__date__gte=dt.date())

        if self.request.GET.get('date_end'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_end'), '%d.%m.%Y')
            te = te.filter(date_start__date__lte=dt.date())
            sum_te = sum_te.filter(date_start__date__lte=dt.date())
            count_te = count_te.filter(date_start__date__lte=dt.date())

        if self.request.GET.get('date_start_e'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_start_e'), '%d.%m.%Y')
            te = te.filter(date_end__date__gte=dt.date())
            sum_te = sum_te.filter(date_end__date__gte=dt.date())
            count_te = count_te.filter(date_end__date__gte=dt.date())

        if self.request.GET.get('date_end_e'):
            dt = datetime.datetime.strptime(self.request.GET.get('date_end_e'), '%d.%m.%Y')
            te = te.filter(date_end__date__lte=dt.date())
            sum_te = sum_te.filter(date_end__date__lte=dt.date())
            count_te = count_te.filter(date_end__date__lte=dt.date())

        if self.request.GET.get('organization'):
            te = te.filter(task__ss_account__name=self.request.GET.get('organization'))
            sum_te = sum_te.filter(task__ss_account__name=self.request.GET.get('organization'))
            count_te = count_te.filter(task__ss_account__name=self.request.GET.get('organization'))

        project = None
        if self.request.GET.get('project'):
            for app in settings.APPLICATIONS:
                if app[1] == self.request.GET.get('project'):
                    project = app[0]
            te = te.filter(application=project)
            sum_te = sum_te.filter(application=project)
            count_te = count_te.filter(application=project)

        q = User.objects.annotate(
            te_exist=Exists(te), te_sum=Subquery(sum_te, output_field=FloatField()),
            te_count=Subquery(count_te, output_field=IntegerField())
        ).filter(te_exist=True).annotate(
            filter_status=Value(self.request.GET.get('status'), output_field=CharField()),
            filter_task=Value(self.request.GET.get('task'), output_field=CharField()),
            filter_exclude_task=Value(self.request.GET.get('exclude_task'), output_field=CharField()),
            filter_date_start=Value(self.request.GET.get('date_start'), output_field=CharField()),
            filter_date_end=Value(self.request.GET.get('date_end'), output_field=CharField()),
            filter_date_start_e=Value(self.request.GET.get('date_start_e'), output_field=CharField()),
            filter_date_end_e=Value(self.request.GET.get('date_end_e'), output_field=CharField()),
            filter_organization=Value(self.request.GET.get('organization'), output_field=CharField()),
            filter_project=Value(project, output_field=CharField()),
        )

        if self.request.GET.get('status_legal'):
            q = q.filter(status_legal=self.request.GET.get('status_legal'))

        if self.request.GET.get('user'):
            q = q.filter(id=self.request.GET.get('user'))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
