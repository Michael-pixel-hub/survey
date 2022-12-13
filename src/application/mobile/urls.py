from django.urls import path

from . import views

app_name = 'mobile'
urlpatterns = [
    path('message/', views.MessageView.as_view(), name='message'),
    path('message/users/count/', views.MessageUsersCountView.as_view(), name='message-users-count'),
]
