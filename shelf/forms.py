from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'categories', 'price', 'size', 'stock', 'description']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
            'size': forms.CheckboxSelectMultiple
        }