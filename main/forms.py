
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
        exclude = ['order','unit_number']

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)

        # Update widget attributes with Tailwind CSS classes
        self.fields['product_type'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['width'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['drop'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['handing'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['box_color'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['fabric_color'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['mounting'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['accessory'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['hand_brace'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['motor_type'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['remote_type'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['fabric_type'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['hardware_color'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['cable_mount'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['cable_size'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})
        self.fields['pile_brush'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded mb-1'})

    