# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, help_text="Escribe algo sobre ti.")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    @property
    def average_rating(self):
        ratings = self.user.received_ratings.all()
        return sum(r.score for r in ratings) / len(ratings) if ratings.exists() else 0
    
class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')  # Nuevo campo
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Valoración de {self.rater.username} a {self.rated.username} ({self.score}/5)"