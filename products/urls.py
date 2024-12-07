#products/urls.py
from django.urls import include, path

from . import views

app_name = 'products'

urlpatterns = [
    
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('<int:product_id>/chat/', views.chat_with_seller, name='chat_with_seller'),
    path('report/<int:product_id>/', views.report_product, name='report_product'),
    path('products/<int:pk>/manage/', views.mark_as_sold_or_withdraw, name='mark_as_sold_or_withdraw'),
    path('products/<int:pk>/assign_buyer/', views.assign_buyer, name='assign_buyer'),
    
]
