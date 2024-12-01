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
    path('admin/reports/', views.admin_report_list, name='admin_report_list'),
    path('admin/reports/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
    path('admin/reviews/', views.admin_review_list, name='admin_review_list'),
    path('admin/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
