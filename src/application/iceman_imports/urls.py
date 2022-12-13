from django.urls import path

from . import views

app_name = 'iceman-imports'

urlpatterns = [
    path('import/stores/', views.ImportStoresView.as_view(), name='import-stores'),
    path('import/products/', views.ImportProductsView.as_view(), name='import-products'),
    path('import/tasks/', views.ImportTasksView.as_view(), name='import-tasks'),
]
