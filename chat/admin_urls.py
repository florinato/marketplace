# chat/admin_urls.py
from django.urls import path

from . import views

app_name = 'admin_chat'

urlpatterns = [
    path('', views.admin_conversation_list, name='admin_conversation_list'),
    path('start/<int:user_id>/', views.start_admin_conversation, name='start_admin_conversation'),
    path('<uuid:pk>/', views.conversation_detail, {'is_admin': True}, name='admin_conversation_detail'),
    path('<uuid:pk>/send/', views.send_message, {'is_admin': True}, name='admin_send_message'),
]
