from datetime import datetime, timedelta
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Order, Store
from .serializers import OrderSerializer, StoreSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'stores': reverse('iceman-api:stores-list', request=request),
        'orders': reverse('iceman-api:orders-list', request=request),
    })


class StoreListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Store.objects.all().prefetch_related(
        'region', 'source', 'iceman_store_document_store', 'iceman_store_stock_store', 'iceman_store_stock_store__stock'
    )
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StoreDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Store.objects.all().prefetch_related(
        'region', 'source', 'iceman_store_document_store', 'iceman_store_stock_store', 'iceman_store_stock_store__stock'
    )
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):

        q = Order.objects.exclude(status=5).prefetch_related(
            'user', 'store', 'store__region', 'store__source', 'store__iceman_store_document_store',
            'store__iceman_store_stock_store', 'store__iceman_store_stock_store__stock', 'iceman_order_product_order',
            'source', 'user__status_iceman'
        )

        if self.kwargs.get('source'):
            q = q.filter(store__source__sys_name=self.kwargs.get('source'))

        if self.request.GET.get('date_create_start'):
            date_create_start = None
            try:
                date_create_start = datetime.strptime(self.request.GET.get('date_create_start'), '%d.%m.%Y %H:%M')
            except:
                pass
            if date_create_start is None:
                try:
                    date_create_start = datetime.strptime(self.request.GET.get('date_create_start'), '%d.%m.%Y')
                except:
                    pass
            if date_create_start is not None:
                q = q.filter(date_create__gte=date_create_start)

        if self.request.GET.get('date_create_end'):
            date_create_end = None
            try:
                date_create_end = datetime.strptime(self.request.GET.get('date_create_end'), '%d.%m.%Y %H:%M')
            except:
                pass
            if date_create_end is None:
                try:
                    date_create_end = datetime.strptime(
                        self.request.GET.get('date_create_end') + ' 23:59:59',
                        '%d.%m.%Y %H:%M:%S')
                except:
                    pass
            if date_create_end is not None:
                q = q.filter(date_create__lte=date_create_end)

        if self.request.GET.get('hours'):
            try:
                hours = int(self.request.GET['hours'])
                date_create = datetime.now() - timedelta(hours=hours)
                q = q.filter(date_create__gte=date_create)
            except:
                pass

        if self.request.GET.get('status'):
            try:
                status = self.request.GET.getlist('status')
                q = q.filter(status__in=status)
            except:
                pass

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all().prefetch_related(
        'user', 'store', 'store__region', 'store__source', 'store__iceman_store_document_store',
        'store__iceman_store_stock_store', 'store__iceman_store_stock_store__stock', 'iceman_order_product_order'
    )
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
