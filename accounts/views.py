from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.forms import ProfileForm
from chat.models import Conversation
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


# Vista principal del perfil con pestañas@login_required
@login_required
def profile(request):
    tab = request.GET.get('tab', 'info')  # Tab por defecto: 'info'
    action = request.GET.get('action', None)  # Acción actual: None o "edit"

    if tab == 'info':
        user_profile = get_object_or_404(Profile, user=request.user)

        # Si estamos en modo edición
        if action == 'edit':
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, instance=user_profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Perfil actualizado correctamente.")
                    return redirect(f"{reverse('profile')}?tab=info")
            else:
                form = ProfileForm(instance=user_profile)
            context = {
                'active_tab': tab,
                'user_profile': user_profile,
                'profile_form': form,
                'editing': True,  # Indica si estamos en modo edición
            }
        else:
            # Modo visualización
            context = {
                'active_tab': tab,
                'user_profile': user_profile,
                'editing': False,
            }

    elif tab == 'products':
        products = Product.objects.filter(user=request.user)
        context = {'active_tab': tab, 'products': products}

    elif tab == 'add_product':
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()

                images = request.FILES.getlist('images')
                for img in images:
                    ProductImage.objects.create(product=product, image=img)

                return redirect(f"{reverse('profile')}?tab=products")
        else:
            product_form = ProductForm()
        context = {'active_tab': tab, 'product_form': product_form}

    elif tab == 'purchases':
        purchases = Product.objects.filter(buyer=request.user)
        context = {'active_tab': tab, 'purchases': purchases}

    elif tab == 'chats':
        conversations = Conversation.objects.filter(participants=request.user)
        conversations_with_unread = [
            {
                'conversation': conv,
                'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count(),
            } for conv in conversations
        ]
        context = {'active_tab': tab, 'conversations': conversations_with_unread}

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

