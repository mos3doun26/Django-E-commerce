from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Full name"}))
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email"}))
    shipping_address_1 = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Address 1"}))
    shipping_address_2 = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Address 2"}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Country"}))
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "City"}))
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "State"}))
    shipping_zip_code = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "ZipCode"}))

    class Meta:
        model =  ShippingAddress
        fields = ["shipping_full_name", 'shipping_email', 'shipping_address_1', "shipping_address_2", "shipping_country","shipping_city", "shipping_state", "shipping_zip_code" ]
        exclude = ['user']
# Here we use form.Form because we don't need to save the billing info in our data base just
# we will pass it to stripe to deal with payments and some security reasons
class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Name on Card"}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Card Number"}))
    expired_date = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Expired Date"}))
    ccv = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "CCV"}))
    country = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Country"}))
    city = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "City"}))
    state = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "State"}))
