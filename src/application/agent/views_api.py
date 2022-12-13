from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from .models import Store, Order, Payment, TinkoffPayment
from .serializers import StoreSerializer, OrderSerializer, PaymentSerializer, TinkoffPaymentSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'stores': reverse('agent-api:store-list', request=request),
        'orders': reverse('agent-api:order-list', request=request),
        'payments': reverse('agent-api:payment-list', request=request),
        'tinkoff-payments': reverse('agent-api:tinkoff-payment-list', request=request),
    })


class StoreListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Store.objects.all().prefetch_related('city', 'user', 'user__rank', 'loyalty_department',
                                                    'loyalty_program', 'category', 'user__status',
                                                    'user__status_agent', 'user__status_iceman')
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StoreDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Store.objects.all().prefetch_related('city', 'user', 'user__rank')
    serializer_class = StoreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all().prefetch_related(
        'user', 'user__rank', 'user__status', 'user__status_agent', 'user__status_iceman',
        'store', 'store__city', 'goods', 'goods__category', 'goods__brand',
        'store__loyalty_department', 'store__loyalty_program', 'store__category'
    )
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all().prefetch_related('user', 'user__rank', 'store', 'store__city', 'goods',
                                                    'goods__category', 'goods__brand')
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PaymentListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self):

        q = Payment.objects.all()

        if self.kwargs.get('day'):
            q = q.filter(date_create__day=self.kwargs.get('day'))
            q = q.filter(date_create__month=self.kwargs.get('month'))
            q = q.filter(date_create__year=self.kwargs.get('year'))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TinkoffPaymentListView(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = TinkoffPaymentSerializer

    def get_queryset(self):

        q = TinkoffPayment.objects.all()

        if self.kwargs.get('day'):
            q = q.filter(date_create__day=self.kwargs.get('day'))
            q = q.filter(date_create__month=self.kwargs.get('month'))
            q = q.filter(date_create__year=self.kwargs.get('year'))

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TinkoffPaymentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = TinkoffPayment.objects.all()
    serializer_class = TinkoffPaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
