
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
    
    
    
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['product_type_manual'].widget = forms.HiddenInput()
        self.fields['width_manual'].widget = forms.HiddenInput()
        self.fields['drop_manual'].widget = forms.HiddenInput()
        self.fields['handing_manual'].widget = forms.HiddenInput()
        self.fields['box_color_manual'].widget = forms.HiddenInput()
        self.fields['fabric_color_manual'].widget = forms.HiddenInput()
        self.fields['mounting_manual'].widget = forms.HiddenInput()

        self.fields['product_type_motorized'].widget = forms.HiddenInput()
        self.fields['width_motorized'].widget = forms.HiddenInput()
        self.fields['drop_motorized'].widget = forms.HiddenInput()
        self.fields['handing_motorized'].widget = forms.HiddenInput()
        self.fields['motor_type'].widget = forms.HiddenInput()
        self.fields['remote_type'].widget = forms.HiddenInput()
        self.fields['box_color_motorized'].widget = forms.HiddenInput()
        self.fields['fabric_type_motorized'].widget = forms.HiddenInput()
        self.fields['fabric_color_motorized'].widget = forms.HiddenInput()
        self.fields['mounting_motorized'].widget = forms.HiddenInput()
        self.fields['hardware_color_motorized'].widget = forms.HiddenInput()
        self.fields['cable_mount_motorized'].widget = forms.HiddenInput()
        self.fields['cable_size_motorized'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        manual_shade = cleaned_data.get("manual_shade")

        if manual_shade:
            self.fields['product_type_manual'].widget = forms.TextInput()
            self.fields['width_manual'].widget = forms.NumberInput()
            self.fields['drop_manual'].widget = forms.NumberInput()
            self.fields['handing_manual'].widget = forms.TextInput()
            self.fields['box_color_manual'].widget = forms.TextInput()
            self.fields['fabric_color_manual'].widget = forms.TextInput()
            self.fields['mounting_manual'].widget = forms.TextInput()
        else:
            self.fields['product_type_motorized'].widget = forms.TextInput()
            self.fields['width_motorized'].widget = forms.NumberInput()
            self.fields['drop_motorized'].widget = forms.NumberInput()
            self.fields['handing_motorized'].widget = forms.TextInput()
            self.fields['motor_type'].widget = forms.TextInput()
            self.fields['remote_type'].widget = forms.TextInput()
            self.fields['box_color_motorized'].widget = forms.TextInput()
            self.fields['fabric_type_motorized'].widget = forms.TextInput()
            self.fields['fabric_color_motorized'].widget = forms.TextInput()
            self.fields['mounting_motorized'].widget = forms.TextInput()
            self.fields['hardware_color_motorized'].widget = forms.TextInput()
            self.fields['cable_mount_motorized'].widget = forms.TextInput()
            self.fields['cable_size_motorized'].widget = forms.TextInput()