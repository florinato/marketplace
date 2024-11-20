from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from products.forms import ProductForm
from products.models import Product  # Importa modelos de productos
from products.models import ProductImage

from .models import Profile


# Registro de usuarios
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


def register(request):
    token = request.GET.get('token', '')
    if token != 'invitacion':
        messages.error(request, "Token de invitación no válido.")
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Garantiza que el perfil se cree junto al usuario
            Profile.objects.get_or_create(user=user)

            login(request, user)
            messages.success(request, "Registro exitoso. Bienvenido a Wallaclone.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Vista principal del perfil con pestañas
@login_required
def profile(request):
    tab = request.GET.get('tab', 'info')  # Tab por defecto: 'info'

    if tab == 'info':
        # Datos para la pestaña de información del usuario
        user_profile = get_object_or_404(Profile, user=request.user)
        context = {'active_tab': tab, 'user_profile': user_profile}

    elif tab == 'products':
        # Productos subidos por el usuario
        products = Product.objects.filter(user=request.user)
        context = {'active_tab': tab, 'products': products}

    elif tab == 'add_product':
        # Lógica para subir producto
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                # Guarda el producto
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()

                # Guarda imágenes adicionales (si existen)
                images = request.FILES.getlist('images')
                for img in images:
                    ProductImage.objects.create(product=product, image=img)

                return redirect(f"{reverse('profile')}?tab=products")
        else:
            product_form = ProductForm()
        
        context = {'active_tab': tab, 'product_form': product_form}

    elif tab == 'purchases':
        # Historial de compras del usuario
        purchases = Product.objects.filter(buyer=request.user)
        context = {'active_tab': tab, 'purchases': purchases}

    elif tab == 'chats':
        # Chats del usuario (lógica pendiente)
        chats = []  # Aquí puedes conectar con el módulo de chat
        context = {'active_tab': tab, 'chats': chats}

    else:
        context = {'active_tab': 'info'}

    return render(request, 'accounts/profile.html', context)


# Historial de compras
@login_required
def purchase_history(request):
    purchases = Product.objects.filter(buyer=request.user)
    return render(request, 'accounts/purchase_history.html', {'purchases': purchases})


# Productos vendidos
@login_required
def sold_products(request):
    sold_products = Product.objects.filter(user=request.user, sold=True)
    return render(request, 'accounts/sold_products.html', {'products': sold_products})

