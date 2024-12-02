#products/urls.py
from django.urls import path

from . import views

urlpatterns = [
    
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('products/<int:pk>/reserve/', views.reserve_product, name='reserve_product'),
    path('<int:product_id>/chat/', views.chat_with_seller, name='chat_with_seller'),
    path('report/<int:product_id>/', views.report_product, name='report_product'),

    

]
