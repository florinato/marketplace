# chat/forms.py

from django import forms

from accounts.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'step': 1, 'class': 'form-control',
                'placeholder': 'Puntúa de 1 a 5'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': 'Deja un comentario sobre el vendedor (opcional)'
            }),
        }
