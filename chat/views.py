# chat/views.py
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Rating
from products.models import Product

from .models import Conversation, Message

logger = logging.getLogger(__name__)

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

    # Recuperar el producto asociado a la conversación
    product = getattr(conversation, 'product', None)

    # Determinar si el usuario puede valorar al vendedor
    has_received_ratings = False
    if product and product.is_sold and product.buyer == request.user:
        # Comprobar si ya existe una valoración para este vendedor y producto
        has_received_ratings = Rating.objects.filter(rater=request.user, rated=product.user, product=product).exists()

    # Recuperar todos los mensajes para mostrar en la conversación
    messages = conversation.messages.all().order_by('timestamp')

    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'product': product,
        'has_received_ratings': has_received_ratings,
        'buyer': product.buyer,
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

@login_required
def rate_seller(request, pk):
    # Obtenemos la conversacion por su UUID
    conversation = get_object_or_404(Conversation, pk=pk)
    product = conversation.product
    seller = product.user

    # Refresh the product object from the database
    product.refresh_from_db()

    logger.info(f"Rating attempt by user: {request.user.username}, buyer: {product.buyer}, is_sold: {product.is_sold}")
    if product.buyer:
        logger.info(f"Product buyer username: {product.buyer.username}")
    logger.info(f"Request user: {request.user}, Request user username: {request.user.username}")

    # Verificar que el request.user es el comprador (product.buyer) y que el producto esta vendido
    if product.buyer != request.user or not product.is_sold:
        messages.error(request, f"No estas autorizado para valorar a este vendedor. product.buyer: {product.buyer}, request.user: {request.user}, product.is_sold: {product.is_sold}")
        return redirect('chat:conversation_detail', pk=conversation.pk)

    # Verificar si ya se ha valorado antes
    if Rating.objects.filter(rater=request.user, rated=seller, product=product).exists():
        messages.info(request, "Ya has valorado a este vendedor.")
        return redirect('chat:conversation_detail', pk=conversation.pk)

    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment', '')
        Rating.objects.create(
            rater=request.user,
            rated=seller,
            product=product,
            score=score,
            comment=comment
        )
        messages.success(request, "¡Gracias por tu valoracion!")
        return redirect('chat:conversation_detail', pk=conversation.pk)

    return render(request, 'chat/rate_seller.html', {
        'product': product,
        'conversation': conversation
    })
