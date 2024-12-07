# products/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from chat.models import Conversation, Message

from .forms import ProductForm, ReportForm
from .models import Product, ProductImage


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        
        if product_form.is_valid():
            # Guarda el producto
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            
            # Guarda las imágenes adicionales (si existen)
            images = request.FILES.getlist('images')  # "images" debe coincidir con el nombre en el formulario
            for img in images:
                ProductImage.objects.create(product=product, image=img)
                
            return redirect('home')  # Redirige al listado de productos
    else:
        product_form = ProductForm()

    return render(request, 'products/add_product.html', {'product_form': product_form})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    
    # Obtener usuarios que han conversado sobre este producto (posibles compradores)
    conversations = Conversation.objects.filter(product=product)
    buyers = User.objects.filter(
        id__in=conversations.values_list('participants', flat=True)
    ).exclude(id=product.user.id)
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'images': images,
        'user': request.user,
        'buyers': buyers,  # Añadimos la lista de compradores potenciales
    })
@login_required
def mark_as_sold_or_withdraw(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == "POST":
        action = request.POST.get('action')  # Recibe "sell" o "withdraw"

        if action == "sell":
            product.is_sold = True
            product.sold_date = timezone.now()

            # Asignar comprador
            buyer_id = request.POST.get('buyer')
            if buyer_id:
                product.buyer = get_object_or_404(User, pk=buyer_id)
                product.save()

                # Crear o buscar conversación
                conversation, created = Conversation.objects.get_or_create(
                    product=product
                )
                conversation.participants.add(request.user, product.buyer)

                # Enviar mensaje automático
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    content=(
                        f"Gracias por tu compra. Por favor, valórame aquí: "
                        f"<a href='{reverse('chat:rate_seller', args=[conversation.pk])}'>Valorar Vendedor</a>"
                    )
                )

            messages.success(request, "Producto marcado como vendido y comprador asignado.")

        elif action == "withdraw":
            product.is_withdrawn = True
            product.is_blocked = True
            product.save()
            messages.success(request, "Producto retirado de la venta.")

        return redirect('products:product_detail', pk=product.pk)


    # Lógica para mostrar el formulario
    buyers = User.objects.filter(
        id__in=Conversation.objects.filter(product=product).values_list('participants', flat=True)
    ).exclude(id=request.user.id)

    return redirect('products:product_detail', pk=product.pk)



@login_required
def assign_buyer(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user, is_sold=True)

    if request.method == "POST":
        buyer_id = request.POST.get('buyer')
        if buyer_id:
            buyer = get_object_or_404(User, pk=buyer_id)
            product.buyer = buyer
            product.save()
            messages.success(request, "Comprador asignado correctamente.")
            return redirect('product_detail', pk=product.pk)
    else:
        # Obtener usuarios que han contactado con el vendedor sobre este producto
        conversations = Conversation.objects.filter(product=product)
        buyers = set()
        for conv in conversations:
            for participant in conv.participants.all():
                if participant != request.user:
                    buyers.add(participant)
        context = {
            'product': product,
            'buyers': buyers
        }
        return render(request, 'products/assign_buyer.html', context)



@login_required
def chat_with_seller(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Verificar si el usuario actual ya tiene una conversación con este producto
    conversation = Conversation.objects.filter(product=product, participants=request.user).first()
    
    if not conversation:
        # Crear una nueva conversación
        conversation = Conversation.objects.create(product=product)
        conversation.participants.add(request.user, product.user)
    
    # Redirigir al sistema de chat
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def report_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reported_user = product.user  # El dueño del producto

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.product = product
            report.save()
            return redirect('product_detail', pk=product.id)
    else:
        form = ReportForm()

    return render(request, 'reports/report_product.html', {
        'form': form,
        'product': product,
    })
