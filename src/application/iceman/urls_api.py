from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import *

app_name = 'iceman-api'
urlpatterns = [
    path('', api_root),
    path('stores/', StoreListView.as_view(), name='stores-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(lookup_field='pk'), name='store-detail'),
    path('orders/', OrderListView.as_view(), name='orders-list'),
    path('orders/source/<str:source>/', OrderListView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(lookup_field='pk'), name='order-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
