from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Conversation, Message


@login_required
def conversation_list(request):
    """Lista todas las conversaciones del usuario."""
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': [
            {
                'conversation': conv,
                'unread_count': conv.unread_messages_count(request.user),
            } for conv in conversations
        ]
    }
    return render(request, 'chat/conversation_list.html', context)


@login_required
def conversation_detail(request, pk):
    """Muestra y gestiona el detalle de una conversación."""
    conversation = get_object_or_404(Conversation, pk=pk)

    # Verificar que el usuario es participante de la conversación
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'No tienes permiso para acceder a esta conversación.'}, status=403)

    # Marcar como leídos solo los mensajes no enviados por el usuario actual
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    # Recuperar todos los mensajes para mostrar en la conversación
    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
    })

@login_required
def send_message(request, pk):
    """Envía un nuevo mensaje en una conversación."""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        content = request.POST.get('content')
        if content:
            # Crear el mensaje sin marcarlo como leído
            Message.objects.create(conversation=conversation, sender=request.user, content=content, is_read=False)
            return redirect('chat:conversation_detail', pk=pk)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def start_conversation(request, product_id):
    """Inicia una conversación entre el usuario actual y el vendedor del producto."""
    product = get_object_or_404(Product, id=product_id)

    # Evitar que el dueño del producto inicie una conversación consigo mismo
    if product.user == request.user:
        return JsonResponse({'error': 'No puedes chatear contigo mismo'}, status=400)

    # Buscar una conversación existente
    conversation = Conversation.objects.filter(product=product, participants=request.user).first()

    if not conversation:
        # Crear una nueva conversación si no existe
        conversation = Conversation.objects.create(product=product)
        conversation.participants.add(request.user, product.user)

    # Redirigir al detalle de la conversación
    return redirect('chat:conversation_detail', pk=conversation.pk)

