# accounts/urls.py

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import CustomLoginForm

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('sold_products/', views.sold_products, name='sold_products'),
    path('admin/reports/', views.admin_report_list, name='admin_report_list'),
    path('admin/reports/resolve/<int:report_id>/', views.resolve_report, name='resolve_report'),
    path('admin/reviews/', views.admin_review_list, name='admin_review_list'),
    path('admin/reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('user/<int:user_id>/', views.user_profile_detail, name='user_profile_detail'),

    # URLs de autenticación
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

