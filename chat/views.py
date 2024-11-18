from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Conversation, Message


@login_required
def conversation_list(request):
    """Lista todas las conversaciones del usuario."""
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, pk):
    """Muestra los detalles de una conversación."""
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = conversation.messages.all()
    return render(request, 'chat/conversation_detail.html', {'conversation': conversation, 'messages': messages})

@login_required
def send_message(request, pk):
    """Envía un nuevo mensaje en una conversación."""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        content = request.POST.get('content')
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
            return redirect('chat:conversation_detail', pk=pk)
    return JsonResponse({'error': 'Invalid request'}, status=400)

