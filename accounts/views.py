from accounts.forms import ProfileForm
from chat.models import AdminConversation, Conversation
from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from products.forms import ProductForm
from products.models import Product, ProductImage, Report

from .models import Profile, Rating


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


@login_required
def profile(request):
    tab = request.GET.get('tab', 'info')  # Tab por defecto: 'info'
    action = request.GET.get('action', None)  # Acción actual

    # Determina si el usuario es admin
    is_admin = request.user.is_staff

    # Contexto inicial
    context = {'active_tab': tab, 'is_admin': is_admin}

    # Tab "info" (Información del usuario)
    if tab == 'info':
        user_profile = get_object_or_404(Profile, user=request.user)

        if action == 'edit':  # Edición de perfil
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, instance=user_profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Perfil actualizado correctamente.")
                    return redirect(f"{reverse('profile')}?tab=info")
            else:
                form = ProfileForm(instance=user_profile)
            context.update({'user_profile': user_profile, 'profile_form': form, 'editing': True})
        else:
            context.update({'user_profile': user_profile, 'editing': False})

    # Tab "products" (Productos del usuario)
    elif tab == 'products':
        products = Product.objects.filter(user=request.user)
        context.update({'products': products})

    # Tab "add_product" (Subir nuevo producto)
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

                messages.success(request, "Producto subido con éxito.")
                return redirect(f"{reverse('profile')}?tab=products")
        else:
            product_form = ProductForm()
        context.update({'product_form': product_form})

    # Tab "purchases" (Productos comprados)
    elif tab == 'purchases':
        purchases = Product.objects.filter(buyer=request.user)
        context.update({'purchases': purchases})

    # Tab "chats" (Conversaciones)
    elif tab == 'chats':
        conversations = Conversation.objects.filter(participants=request.user)
        conversations_with_unread = [
            {
                'conversation': conv,
                'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count(),
                'product_image': conv.product.main_image.url if conv.product and conv.product.main_image else None,
            } for conv in conversations
        ]
        context.update({'conversations': conversations_with_unread})

    # Tab "admin" (Panel de administración)
    elif tab == 'admin' and is_admin:
        reports = Report.objects.filter(status='pending').order_by('-created_at')
        reviews = Rating.objects.all().order_by('-created_at')
        admin_conversations = AdminConversation.objects.filter(participants=request.user)
        context.update({'reports': reports, 'reviews': reviews, 'admin_conversations': admin_conversations})

    # Render de la plantilla con el contexto
    return render(request, 'accounts/profile.html', context)


# Historial de compras
@login_required
def purchase_history(request):
    purchases = Product.objects.filter(buyer=request.user)
    return render(request, 'accounts/purchase_history.html', {'purchases': purchases})


# Productos vendidos
@login_required
def sold_products(request):
    sold_products = Product.objects.filter(user=request.user, is_sold=True)
    return render(request, 'accounts/sold_products.html', {'products': sold_products})


@login_required
def admin_report_list(request):
    if not request.user.is_staff:
        return redirect('home')

    reports = Report.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'admin/report_list.html', {'reports': reports})


@login_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    # Solo permitir que admins gestionen reportes
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para realizar esta acción.")
        return redirect('profile')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'resolve':
            report.status = 'resolved'
            messages.success(request, f"El reporte sobre {report.product.title} ha sido resuelto.")
        elif action == 'dismiss':
            report.status = 'dismissed'
            messages.info(request, f"El reporte sobre {report.product.title} ha sido descartado.")
        report.save()

    # Redirigir al perfil con la pestaña de administración activa
    return redirect(f"{reverse('accounts:profile')}?tab=admin")


@login_required
def admin_review_list(request):
    if not request.user.is_staff:
        return redirect('home')

    reviews = Rating.objects.all().order_by('-created_at')
    return render(request, 'admin/review_list.html', {'reviews': reviews})


@login_required
def delete_review(request, review_id):
    if not request.user.is_staff:
        return redirect('home')

    review = get_object_or_404(Rating, pk=review_id)
    review.delete()
    return redirect('admin_review_list')


def user_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    sold_products = Product.objects.filter(user=user, is_sold=True)
    ratings = Rating.objects.filter(rated=user)

    # Cálculo del promedio usando agregación
    average_rating = ratings.aggregate(avg_rating=Avg('score'))['avg_rating'] or 0

    context = {
        'profile_user': user,
        'sold_products': sold_products,
        'ratings': ratings,
        'average_rating': round(average_rating, 1),  # Redondeo a un decimal
    }
    return render(request, 'accounts/user_profile_detail.html', context)
