from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import *

app_name = 'agent-api'
urlpatterns = [
    path('', api_root),
    path('stores/', StoreListView.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(lookup_field='pk'), name='store-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(lookup_field='pk'), name='order-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/date/<int:day>.<int:month>.<int:year>/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(lookup_field='pk'), name='payment-detail'),
    path('tinkoff-payments/', TinkoffPaymentListView.as_view(), name='tinkoff-payment-list'),
    path('tinkoff-payments/date/<int:day>.<int:month>.<int:year>/', TinkoffPaymentListView.as_view(),
         name='tinkoff-payment-list'),
    path('tinkoff-payments/<int:pk>/', TinkoffPaymentDetailView.as_view(lookup_field='pk'),
         name='tinkoff-payment-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
