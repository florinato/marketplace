from django.contrib.auth.models import User
from django.db import models

from products.models import \
    Product  # Si las conversaciones están asociadas a productos


class Conversation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations')
    participants = models.ManyToManyField('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación sobre {self.product.title} - {self.created_at}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.username} en {self.conversation.product.title}"

