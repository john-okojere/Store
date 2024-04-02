from django import forms
from .models import CartItem

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.product.stock:
            raise forms.ValidationError("Sorry, there is not enough stock for this product.")
        return quantity

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
        }