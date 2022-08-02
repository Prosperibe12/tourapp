from cProfile import label
from django import forms 
from . models import *

class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ['cart', 'amount', 'order_status', 'discount', 'subtotal', 'payment_completed', 'ref']
        widgets = {
            'ordered_by': forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'payment_method': forms.TextInput(attrs={'class':'form-control'})
        }