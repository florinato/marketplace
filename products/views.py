# products/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import Conversation

from .forms import ProductForm
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
    return render(request, 'products/product_detail.html', {
        'product': product,
        'images': images,
        'user': request.user,
    })

@login_required
def reserve_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product.is_reserved:  # O un campo similar para verificar si está reservado
        product.is_reserved = True
        product.buyer = request.user
        product.save()
        messages.success(request, "Has reservado este producto exitosamente.")
    else:
        messages.error(request, "Este producto ya está reservado.")
    return redirect('product_detail', product_id=product.id)

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

