# marketplace/views.py
from django.shortcuts import render

from products.models import Product


def home(request):
    status_filter = request.GET.get('status', 'available')  # Default to 'available'

    if status_filter == 'available':
        products = Product.objects.filter(is_sold=False, is_blocked=False, is_withdrawn=False)
    elif status_filter == 'sold':
        products = Product.objects.filter(is_sold=True)
    elif status_filter == 'blocked':
        products = Product.objects.filter(is_blocked=True)
    elif status_filter == 'withdrawn':
        products = Product.objects.filter(is_withdrawn=True)
    elif status_filter == 'all':
        products = Product.objects.all()
    else:  # Default to 'available' if the filter is invalid
        products = Product.objects.filter(is_sold=False, is_blocked=False, is_withdrawn=False)


    return render(request, 'marketplace/home.html', {'products': products, 'status_filter': status_filter})
