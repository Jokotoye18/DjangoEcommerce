from django import forms
from .models import BillingAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_METHOD = (
    ('S', 'stripe'),
    ('P', 'paypal')
)

class BillingAddressForm(forms.ModelForm):
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}), required=False)
    payment_options = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_METHOD)


    class Meta:
        model = BillingAddress
        fields = ['street_address', 'apartment_address', 'country', 'zip', 'same_billing_address', 'save_info', 'payment_options']
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder':'1234 Main St', 'class':'form-control'}),
            'apartment_address': forms.TextInput(attrs={'placeholder':'Apartment or suite', 'class':'form-control'}),
            'zip': forms.TextInput(attrs={'class':'form-control'}),
            'country': CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'})
        }