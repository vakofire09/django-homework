from django import forms
from .models import Product
from .models import ProductRating

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'discount', 'in_stock', 'image', 'brand']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True})
        }