# chat/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Rating
from products.models import Product

from .models import AdminConversation, AdminMessage, Conversation, Message


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': [
            {
                'conversation': conv,
                'unread_count': conv.unread_messages_count(request.user),
                'product_image': conv.product.image.url if conv.product.image else None,
            } for conv in conversations
        ]
    }
    return render(request, 'chat/conversation_list.html', context)

# ... otras vistas ...
@login_required
def admin_conversation_list(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permisos para acceder a esta sección'}, status=403)
    conversations = AdminConversation.objects.filter(participants=request.user)
    context = {
        'conversations': [
            {
                'conversation': conv,
                'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count()
            } for conv in conversations
        ]
    }
    return render(request, 'chat/admin_conversation_list.html', context)

@login_required
def start_conversation(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user == request.user:
        return JsonResponse({'error': 'No puedes chatear contigo mismo'}, status=400)
    conversation = Conversation.objects.filter(product=product, participants=request.user).first()
    if not conversation:
        conversation = Conversation.objects.create(product=product)
        conversation.participants.add(request.user, product.user)
    return redirect('chat:conversation_detail', pk=conversation.pk)

@login_required
def start_admin_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation, created = AdminConversation.objects.get_or_create(
        defaults={'created_at': timezone.now()}
    )
    conversation.participants.add(request.user, other_user)
    return redirect('admin_chat:admin_conversation_detail', pk=conversation.uuid)

@login_required
def conversation_detail(request, pk, is_admin=False):
    if is_admin:
        conversation = get_object_or_404(AdminConversation, uuid=pk)
        messages = AdminMessage.objects.filter(conversation=conversation).order_by('created_at')
    else:
        conversation = get_object_or_404(Conversation, id=pk)
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'No autorizado.'}, status=403)
    if not is_admin:
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    context = {
        'conversation': conversation,
        'messages': messages,
        'is_admin': is_admin,
    }
    return render(request, 'chat/conversation_detail.html', context)

@login_required
def send_message(request, pk, is_admin=False):
    if request.method == 'POST':
        if is_admin:
            conversation = get_object_or_404(AdminConversation, uuid=pk)
            AdminMessage.objects.create(
                conversation=conversation,
                sender=request.user,
                message=request.POST.get('content')
            )
            return redirect('admin_chat:admin_conversation_detail', pk=conversation.uuid)
        else:
            conversation = get_object_or_404(Conversation, id=pk, participants=request.user)
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=request.POST.get('content')
            )
            return redirect('chat:conversation_detail', pk=conversation.pk)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def rate_seller(request, pk):
    # Obtenemos la conversacion por su UUID
    conversation = get_object_or_404(Conversation, pk=pk)
    product = conversation.product
    seller = product.user

    # Verificar que el request.user es el comprador (product.buyer) y que el producto esta vendido
    if product.buyer != request.user or not product.is_sold:
        messages.error(request, "No estas autorizado para valorar a este vendedor.")
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
@login_required
def start_conversation_with_user(request, user_id):
    """Inicia o redirige a una conversación administrativa."""
    other_user = get_object_or_404(User, id=user_id)

    # Busca o crea una conversación administrativa
    conversation, created = Conversation.objects.get_or_create(
        product=None,
        defaults={'created_at': timezone.now()}
    )
    conversation.participants.add(request.user, other_user)

    # Redirige al detalle de la conversación
    return redirect('chat:conversation_detail', pk=conversation.pk)
from .models import AdminConversation, AdminMessage


@login_required
def admin_conversation_list(request):
    """Lista todas las conversaciones administrativas del administrador."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permisos para acceder a esta sección'}, status=403)

    conversations = AdminConversation.objects.filter(participants=request.user)
    context = {
        'conversations': [
            {
                'conversation': conv,
                'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count()
            } for conv in conversations
        ]
    }
    return render(request, 'chat/admin_conversation_list.html', context)
@login_required
def start_admin_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation, created = AdminConversation.objects.get_or_create(
        defaults={'created_at': timezone.now()}
    )
    conversation.participants.add(request.user, other_user)
    return redirect('chat:conversation_detail', pk=conversation.uuid, is_admin=True)


