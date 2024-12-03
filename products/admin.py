from django.contrib import admin

from .models import Product, ProductImage, Report


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'user', 'condition')
    list_filter = ('condition', 'tags')
    search_fields = ('title', 'description', 'tags')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__title',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reason', 'reporter__username', 'reported_user__username', 'product__title')
