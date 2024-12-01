# marketplace/views.py
from django.shortcuts import render

from products.models import Product


def home(request):
    # Excluye productos bloqueados o vendidos
    products = Product.objects.filter(is_sold=False).exclude(is_blocked=True)

    return render(request, 'marketplace/home.html', {'products': products})