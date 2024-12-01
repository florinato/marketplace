# accounts/admin.py

from django.contrib import admin

from .models import Profile, Rating


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'average_rating')
    search_fields = ('user__username',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rater', 'rated', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('rater__username', 'rated__username', 'comment')


