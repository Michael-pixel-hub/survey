from django.urls import path

from . import views

app_name = 'iceman'
urlpatterns = [
    path('message/', views.MessageView.as_view(), name='message'),
    path('message/users/count/', views.MessageUsersCountView.as_view(), name='message-users-count'),

    path('export/stores/', views.ExportStoresView.as_view(), name='export-stores'),
    path('export/tasks/', views.ExportTasksView.as_view(), name='export-tasks'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('reports/icemans/', views.ReportIcemansView.as_view(), name='report_icemans'),
    path('reports/icemans/tasklist', views.IcemanTaskListReportView.as_view(), name='report-tasklist'),
]

urlpatterns += [
    path('autocomplete/usersubs/', views.UserSubsAutocompleteView.as_view(), name='ac-usersubs'),
    path('autocomplete/regions/', views.RegionsAutocompleteView.as_view(), name='ac-regions'),
    path('autocomplete/statusiceman/', views.StatusIcemanAutocompleteView.as_view(), name='ac-statusiceman'),
    path('autocomplete/taskisdone/', views.TaskIsdoneAutocompleteView.as_view(), name='ac-taskisdone'),
    path('autocomplete/usersdevice/', views.UsersDeviceAutocompleteView.as_view(), name='ac-usersdevice'),
]
