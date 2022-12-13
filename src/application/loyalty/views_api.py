from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Department, Program, Store
from .serializers import DepartmentSerializer, ProgramSerializer, StoreSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'departments': reverse('loyalty-api:department-list', request=request),
        'programs': reverse('loyalty-api:program-list', request=request),
        'stores': reverse('loyalty-api:store-list', request=request),
    })


class DepartmentListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Department.objects.filter(is_public=True)
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DepartmentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProgramListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Program.objects.filter(is_public=True)
    serializer_class = ProgramSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProgramDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StoreListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Store.objects.prefetch_related('loyalty_department', 'loyalty_program', )
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StoreDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Store.objects.prefetch_related('loyalty_department', 'loyalty_program', )
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

