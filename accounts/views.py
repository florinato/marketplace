from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Profile


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
    """Vista para mostrar y actualizar el perfil del usuario."""
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Formulario para actualizar el perfil
        bio = request.POST.get('bio', user_profile.bio)
        profile_image = request.FILES.get('profile_image', user_profile.profile_image)

        user_profile.bio = bio
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()

        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': user_profile})




