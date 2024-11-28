from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address_line1", "address_line2", "city", "state", "zip_code", "country"]
        widgets = {
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
