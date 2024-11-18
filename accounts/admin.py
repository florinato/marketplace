# accounts/admin.py

from django.contrib import admin

from products.models import Product, ProductImage

from .models import Profile

# Registra ambos modelos
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Profile)

