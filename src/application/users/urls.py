from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('password/', views.UserChangePasswordView.as_view(), name='password'),
]
