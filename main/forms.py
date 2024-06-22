
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Timeline, Unit, Order

class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['type', 'comment']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'account_name', 'po_number', 'ship_to', 'shipping_address', 'city', 
            'state', 'zip_code', 'phone', 'ship_via', 'installation_address', 'installation_address_same_as_shipping'
        ]
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['account_name'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['po_number'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['ship_to'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['shipping_address'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['city'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['state'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['zip_code'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['phone'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['ship_via'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['installation_address'].widget.attrs.update({'class': 'inadd w-full p-2 border border-gray-300 rounded mb-1', 'disabled':True})
        self.fields['installation_address_same_as_shipping'].widget.attrs.update({'class': 'sameship p-2 border border-gray-300 rounded mb-1'})
    

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['product_type'].widget = forms.HiddenInput()
        self.fields['width'].widget = forms.HiddenInput()
        self.fields['drop'].widget = forms.HiddenInput()
        self.fields['handing'].widget = forms.HiddenInput()
        self.fields['box_color'].widget = forms.HiddenInput()
        self.fields['fabric_color'].widget = forms.HiddenInput()
        self.fields['mounting'].widget = forms.HiddenInput()
        self.fields['motor_type'].widget = forms.HiddenInput()
        self.fields['remote_type'].widget = forms.HiddenInput()
        self.fields['hardware_color'].widget = forms.HiddenInput()
        self.fields['cable_mount'].widget = forms.HiddenInput()
        self.fields['cable_size'].widget = forms.HiddenInput()
        self.fields['pile_brush'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        manual_shade = cleaned_data.get("manual_shade")

        self.fields['product_type'].widget = forms.Select(choices=self.fields['product_type'].choices)
        self.fields['width'].widget = forms.NumberInput()
        self.fields['drop'].widget = forms.NumberInput()
        self.fields['handing'].widget = forms.Select(choices=self.fields['handing'].choices)
        self.fields['box_color'].widget = forms.Select(choices=self.fields['box_color'].choices)
        self.fields['fabric_color'].widget = forms.Select(choices=self.fields['fabric_color'].choices)
        self.fields['mounting'].widget = forms.Select(choices=self.fields['mounting'].choices)
        self.fields['product_type'].widget = forms.Select(choices=self.fields['product_type'].choices)
        self.fields['motor_type'].widget = forms.Select(choices=self.fields['motor_type'].choices)
        self.fields['remote_type'].widget = forms.Select(choices=self.fields['remote_type'].choices)
        self.fields['fabric_type'].widget = forms.Select(choices=self.fields['fabric_type'].choices)
        self.fields['hardware_color'].widget = forms.Select(choices=self.fields['hardware_color'].choices)
        self.fields['cable_mount'].widget = forms.Select(choices=self.fields['cable_mount'].choices)
        self.fields['cable_size'].widget = forms.Select(choices=self.fields['cable_size'].choices)
        self.fields['pile_brush'].widget = forms.Select(choices=self.fields['pile_brush'].choices)

    def save(self, commit=True):
        instance = super(UnitForm, self).save(commit=False)
        if instance.manual_shade:
            instance.motor_type = None
            instance.remote_type = None
        if commit:
            instance.save()
        return instance