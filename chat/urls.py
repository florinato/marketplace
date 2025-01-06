# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', views.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', views.send_message, name='send_message'),
    path('start/<int:product_id>/', views.start_conversation, name='start_conversation'),
    path('close_product_conversations/<int:product_id>/', views.close_product_conversations, name='close_product_conversations'),
    path('<uuid:pk>/rate_seller/', views.rate_seller, name='rate_seller'),
]
