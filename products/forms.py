# products/forms.py

from django import forms

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