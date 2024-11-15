#products/urls.py
from django.urls import path

from . import views

urlpatterns = [
    
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    
]
