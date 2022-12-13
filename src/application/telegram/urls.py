from django.urls import path

from . import views

app_name = 'telegram'
urlpatterns = [
    path('message/', views.MessageView.as_view(), name='message'),
    path('message-group/', views.MessageGroupView.as_view(), name='message_group'),
    path('message-group-file/', views.MessageGroupFileView.as_view(), name='message_group_file'),
    path('message-stores/', views.MessageStoresView.as_view(), name='message_stores'),
    path('message-stores-file/', views.MessageStoresFileView.as_view(), name='message_stores_file'),
]
