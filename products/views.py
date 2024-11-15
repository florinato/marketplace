from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, ProductImageForm
from .models import Product, ProductImage

# products/views.py

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
    return render(request, 'products/product_detail.html', {'product': product, 'images': images})





