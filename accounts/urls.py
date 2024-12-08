# accounts/urls.py

from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/purchase-history/', views.purchase_history, name='purchase_history'),
    path('profile/sold-products/', views.sold_products, name='sold_products'),
    path('user/<int:user_id>/', views.user_profile_detail, name='user_profile_detail'),

]
