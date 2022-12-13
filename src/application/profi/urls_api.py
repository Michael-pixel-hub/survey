from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import *

app_name = 'profi-api'
urlpatterns = [
    path('', api_root),
    path('strings/', StringListView.as_view(), name='string-list'),
    path('strings/<int:pk>/', StringDetailView.as_view(lookup_field='pk'), name='string-detail'),
    path('strings/<slug:slug>/', StringDetailView.as_view(lookup_field='slug'), name='string-detail'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(lookup_field='pk'), name='user-detail'),
    path('users/telegram/<slug:telegram_id>/', UserDetailView.as_view(lookup_field='telegram_id'), name='user-detail'),
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('reports/user/<int:user_id>/', ReportListView.as_view(), name='report-list'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/author/<int:author_id>/', TaskListView.as_view(), name='task-list'),
    path('calc/', CalcView.as_view(), name='calc'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/user/<int:user_id>/', OrderListView.as_view(), name='order-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
