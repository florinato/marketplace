from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe algo sobre ti...',
                'rows': 3,
            }),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
