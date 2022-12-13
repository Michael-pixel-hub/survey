from django.urls import path

from . import views

app_name = 'profi'
urlpatterns = [
    path('message/', views.MessageView.as_view(), name='message'),
]
