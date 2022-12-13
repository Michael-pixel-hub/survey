from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import *


app_name = 'survey-api'
urlpatterns = [
    path('', api_root),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/tasks/', UsersTasksListView.as_view(), name='users-tasks'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/search/<str:search>/', ClientListView.as_view(), name='client-list'),
    path('ranks/', RankListView.as_view(), name='rank-list'),
    path('ranks/<int:pk>/', RankDetailView.as_view(), name='rank-detail'),
    path('ranks/search/<str:search>/', RankListView.as_view(), name='rank-list'),
    path('regions/', RegionListView.as_view(), name='region-list'),
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),
    path('regions/search/<str:search>/', RegionListView.as_view(), name='region-list'),
    path('stores/', StoreListView.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
    path('stores/geo/<str:longitude>:<str:latitude>/', StoreListView.as_view(), name='report-list'),
    path('goods/', GoodListView.as_view(), name='good-list'),
    path('goods/<int:pk>/', GoodDetailView.as_view(), name='good-detail'),
    path('inspector/goods/', InspectorGoodListView.as_view(), name='inspector-good-list'),
    path('inspector/goods/<int:pk>/', InspectorGoodDetailView.as_view(), name='inspector-good-detail'),
    # path('inspector/before/', InspectorBeforeListView.as_view(), name='inspector-before-list'),
    # path('inspector/before/<int:pk>/', InspectorBeforeDetailView.as_view(), name='inspector-before-detail'),
    path('assortments/', AssortmentListView.as_view(), name='assortment-list'),
    path('assortments/<int:pk>/', AssortmentDetailView.as_view(), name='assortment-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks-execution/', TasksExecutionListView.as_view(), name='task-execution-list'),
    path('tasks-execution/<int:pk>/', TasksExecutionDetailView.as_view(), name='task-execution-detail'),
    path('store-tasks/', StoreTaskListView.as_view(), name='store-task-list'),
    path('store-tasks/<int:pk>/', StoreTaskDetailView.as_view(), name='store-task-detail'),
    path('acts/', ActListView.as_view(), name='act-list'),
    path('acts/<int:pk>/', ActDetailView.as_view(), name='act-detail'),

    path('public/user/', PublicUserCreateView.as_view(), name='public-user'),
    path('public/user/<str:api_key>/', PublicUserDetailView.as_view(), name='public-user-detail'),
    path('public/clients/', PublicClientListView.as_view(), name='public-client-list'),
    path('public/clients/<int:pk>/', PublicClientDetailView.as_view(), name='public-client-detail'),
    path('public/clients/search/<str:search>/', PublicClientListView.as_view(), name='public-client-list'),
    path('public/categories/', PublicCategoryListView.as_view(), name='public-category-list'),
    path('public/categories/<int:pk>/', PublicCategoryDetailView.as_view(), name='public-category-detail'),
    path('public/categories/search/<str:search>/', PublicCategoryListView.as_view(), name='public-category-list'),
    path('public/regions/', PublicRegionListView.as_view(), name='public-region-list'),
    path('public/regions/<int:pk>/', PublicRegionDetailView.as_view(), name='public-region-detail'),
    path('public/regions/search/<str:search>/', PublicRegionListView.as_view(), name='public-region-list'),
    path('public/stores/', PublicStoreListView.as_view(), name='public-store-list'),
    path('public/stores/<int:pk>/', PublicStoreDetailView.as_view(), name='public-store-detail'),
    path('public/stores/geo/<str:longitude>:<str:latitude>/', PublicStoreListView.as_view(), name='public-store-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
