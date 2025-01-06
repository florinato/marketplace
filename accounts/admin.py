from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Conversation

from .models import Profile, Rating


class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        if change and not obj.is_active and form.initial['is_active']:
            # User is being deactivated (blocked)
            conversations = Conversation.objects.filter(
                Q(participants=obj) & Q(closed_at__isnull=True)
            )
            for conversation in conversations:
                conversation.close()
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'average_rating')
    search_fields = ('user__username',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rater', 'rated', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('rater__username', 'rated__username', 'comment')
