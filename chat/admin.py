from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    search_fields = ('product__title', 'participants__username')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'sender', 'timestamp')
    search_fields = ('conversation__product__title', 'sender__username')


