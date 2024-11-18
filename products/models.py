# products/models.py
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, blank=True, null=True, default="Nuevo")
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True, default="")

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(self.image.path)

    def __str__(self):
        return f"Imagen de {self.product.title}"


    

