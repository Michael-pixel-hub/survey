from django.db.models import Q

from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


from .models import String, User, Menu, Report, Task, Order
from .serializers import StringSerializer, UserSerializer, MenuSerializer, ReportSerializer, TaskSerializer, Calc, \
    OrderSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('profi-api:user-list', request=request),
        'strings': reverse('profi-api:string-list', request=request),
        'menu': reverse('profi-api:menu-list', request=request),
        'reports': reverse('profi-api:report-list', request=request),
        'tasks': reverse('profi-api:task-list', request=request),
        'orders': reverse('profi-api:order-list', request=request),
    })


class StringListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = String.objects.all()
    serializer_class = StringSerializer
    lookup_field = 'slug'
    paginator = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StringDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = String.objects.all()
    serializer_class = StringSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MenuListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Menu.objects.filter(is_public=True)
    serializer_class = MenuSerializer
    paginator = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MenuDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Menu.objects.filter(is_public=True)
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserMixin(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        if request.data.get('telegram', {}).get('is_telegram') is not None:
            request.data['is_telegram'] = request.data.get('telegram', {}).get('is_telegram')
        if request.data.get('telegram', {}).get('id') is not None:
            request.data['telegram_id'] = request.data.get('telegram', {}).get('id')
        if request.data.get('telegram', {}).get('language_code') is not None:
            request.data['telegram_language_code'] = request.data.get('telegram', {}).get('language_code')
        if request.data.get('telegram', {}).get('last_name') is not None:
            request.data['telegram_last_name'] = request.data.get('telegram', {}).get('last_name')
        if request.data.get('telegram', {}).get('first_name') is not None:
            request.data['telegram_first_name'] = request.data.get('telegram', {}).get('first_name')
        if request.data.get('telegram', {}).get('username') is not None:
            request.data['telegram_username'] = request.data.get('telegram', {}).get('username')


class UserListView(UserMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'telegram_id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class UserDetailView(UserMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'telegram_id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReportListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        q = Report.objects.all().prefetch_related('user')
        if self.kwargs.get('user_id'):
            q = q.filter(user__id=self.kwargs.get('user_id'))
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReportDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TaskListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        q = Task.objects.filter(is_public=True).prefetch_related('author')
        if self.kwargs.get('author_id'):
            q = q.filter(Q(author__id=self.kwargs.get('author_id')) | Q(author__id__isnull=True))
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.data.get('author') is not None:
            request.data['author_id'] = request.data.get('author')
        return self.create(request, *args, **kwargs)


class TaskDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Task.objects.filter(is_public=True)
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CalcView(APIView):

    def get(self, request, *args, **kw):

        task = request.GET.get('task', None)
        stores = request.GET.get('stores', None)
        regions = request.GET.get('regions', None)
        clients = request.GET.get('clients', None)

        calc = Calc(task=task, stores=stores, regions=regions, clients=clients, *args, **kw)
        result = calc.calc()
        response = Response(result, status=status.HTTP_200_OK)

        return response


class OrderListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):
        q = Order.objects.all().prefetch_related('user', 'task', 'clients', 'regions', 'stores', 'stores__client',
                                                 'stores__region_o')
        if self.kwargs.get('user_id'):
            q = q.filter(user__id=self.kwargs.get('user_id'))
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.data)
        s = OrderSerializer(data=request.data)
        print(s.is_valid())
        print(s.errors)
        return self.create(request, *args, **kwargs)


class OrderDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
