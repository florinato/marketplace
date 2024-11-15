from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.all()  # Consulta los productos para mostrar en el inicio
    return render(request, 'main/home.html', {'products': products})
