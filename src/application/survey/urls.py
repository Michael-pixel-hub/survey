from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('data/import/', views.ImportView.as_view(), name='import'),
    path('data/import/tasks/', views.ImportTasksView.as_view(), name='import-tasks'),
    path('data/export/', views.ExportView.as_view(), name='export'),
    path('data/reports/', views.ReportsView.as_view(), name='reports'),
    path('data/reports/task_execution/', views.ReportTeView.as_view(), name='report_te'),
    path('data/reports/declines/', views.ReportTeDeclinesView.as_view(), name='reports_declines'),
    path('data/reports/orders/', views.ReportOrdersView.as_view(), name='report_agent_orders'),
    path('data/reports/surveyors/', views.ReportSurveyorsView.as_view(), name='report_surveyors'),
    path('data/reports/devicesurveyors/', views.ReportDeviceSurveyorsView.as_view(), name='report_devicesurveyors'),
    path('data/reports/taxpayers/', views.ReportTaxpayersView.as_view(), name='report_taxpayers'),
    path('data/reports/acts/', views.ReportActsView.as_view(), name='report_acts'),
    path('data/reports/auditors/', views.ReportAuditorsView.as_view(), name='report_auditors'),
    path('data/images/', views.DownloadImages.as_view(), name='download_images'),
    path('data/images/count/', views.DownloadImagesCount.as_view(), name='download_images_count'),
    path('data/users/count/', views.DownloadImagesCount.as_view(), name='message_users_count'),
]

urlpatterns += [
    path('autocomplete/clients/', views.TaskClientsAutocompleteView.as_view(), name='ac-clients'),
    path('autocomplete/stores/', views.TaskStoresAutocompleteView.as_view(), name='ac-stores'),
    path('autocomplete/regions/', views.TaskRegionsAutocompleteView.as_view(), name='ac-regions'),
    path('autocomplete/users/', views.UsersAutocompleteView.as_view(), name='ac-users'),
    path('autocomplete/usersdevice/', views.UsersDeviceAutocompleteView.as_view(), name='ac-usersdevice'),
    path('autocomplete/tasks/', views.TasksAutocompleteView.as_view(), name='ac-tasks'),
    path('autocomplete/ranks/', views.RanksAutocompleteView.as_view(), name='ac-ranks'),
    path('autocomplete/usersubs/', views.UserSubsAutocompleteView.as_view(), name='ac-usersubs'),
    path('autocomplete/imagestep/', views.ImageStepAutocompleteView.as_view(), name='ac-imagestep'),
    path('autocomplete/userstatus/', views.UserStatusAutocompleteView.as_view(), name='ac-userstatus'),
]


urlpatterns += [
    path('map/old/', views.MapView.as_view()),
    path('map/', views.OSMMapView.as_view(), name='map'),
    path('map/smoroza/', views.SmorozaMapView.as_view(), name='map-smoroza'),
    path('1c/upload/', views.Upload1cView.as_view(), name='1c'),
    path('do/request/', views.ExternalRequestView.as_view(), name='1c'),
    # path('map/json/', views.JSONMapView.as_view(), name='map-json'),
]
