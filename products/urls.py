from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/mark_as_sold_or_withdraw/', views.mark_as_sold_or_withdraw, name='mark_as_sold_or_withdraw'),
    path('<int:product_id>/report/', views.report_product, name='product_report'),
    path('add/', views.add_product, name='add_product'),
    path('api/products/', views.get_products_api, name='get_products_api'),
]
