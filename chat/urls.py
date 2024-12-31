# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('start/<int:product_id>/', views.start_conversation, name='start_conversation'),
    path('<uuid:pk>/', views.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', views.send_message, name='send_message'),
]
