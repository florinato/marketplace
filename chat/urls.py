# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', views.conversation_detail, name='conversation_detail'),  # Cambiado de <int:pk> a <uuid:pk>
    path('<uuid:pk>/send/', views.send_message, name='send_message'),  # Cambiado de <int:pk> a <uuid:pk>
    path('start/<int:product_id>/', views.start_conversation, name='start_conversation'),
]
