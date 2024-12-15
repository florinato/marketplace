# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('start/<int:product_id>/', views.start_conversation, name='start_conversation'),
    path('<uuid:pk>/', views.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', views.send_message, name='send_message'),  # Ruta para enviar mensaje
    path('admin/<uuid:pk>/', views.conversation_detail, {'is_admin': True}, name='admin_conversation_detail'),
    path('admin/start/<int:user_id>/', views.start_admin_conversation, name='start_admin_conversation'),
    path('start_user/<int:user_id>/', views.start_conversation_with_user, name='start_user_conversation'),
]