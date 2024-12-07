# products/forms.py

from django import forms
from django.contrib.auth.models import User

from .models import Product, ProductImage, Report


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'condition', 'main_image', 'tags']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']  # Solo pedimos el motivo
        widgets = {
            'reason': forms.Textarea(attrs={
                'placeholder': 'Escribe el motivo del reporte aquí...',
                'rows': 4,
                'class': 'form-control',
            }),
        }
class MarkAsSoldForm(forms.Form):
    buyer = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Seleccionar comprador",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        user_queryset = kwargs.pop('user_queryset', User.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = user_queryset
