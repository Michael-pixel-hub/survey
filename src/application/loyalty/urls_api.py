from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import *

app_name = 'loyalty-api'
urlpatterns = [
    path('', api_root),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(lookup_field='pk'), name='department-detail'),
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(lookup_field='pk'), name='program-detail'),
    path('stores/', StoreListView.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(lookup_field='pk'), name='store-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
