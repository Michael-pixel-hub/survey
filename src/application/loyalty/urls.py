from django.urls import path

from . import views

app_name = 'loyalty'
urlpatterns = [
    path('data/reports/stores/', views.ReportStoresView.as_view(), name='report_stores'),
]
