# chat/models.py
import uuid  # Para generar UUIDs únicos

from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID como clave primaria
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='conversations', null=True, blank=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación sobre {self.product.title if self.product else 'usuarios'} - {self.created_at}"

    def unread_messages_count(self, user):
        # Contar solo mensajes enviados por otros y no leídos por el usuario actual
        return self.messages.filter(is_read=False).exclude(sender=user).count()




class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"Mensaje de {self.sender.username} en {self.conversation.product.title}"
class AdminConversation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    participants = models.ManyToManyField(User, related_name='admin_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class AdminMessage(models.Model):
    conversation = models.ForeignKey(AdminConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

