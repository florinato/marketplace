# products/admin.py

from django.contrib import admin

from products.models import Product, ProductImage

# Registra ambos modelos
admin.site.register(Product)
admin.site.register(ProductImage)

