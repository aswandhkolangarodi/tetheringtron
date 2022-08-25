from django import forms
from member.models import Kyc
from django.forms.widgets import SelectMultiple, TextInput, Textarea, EmailInput, CheckboxInput, URLInput, Select, NumberInput, RadioSelect, FileInput, ClearableFileInput


class KycForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'required': 'required', 'autocomplete': 'off', 'placeholder': 'Your Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': 'required', 'autocomplete': 'off', 'placeholder': 'Your Email'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'required': 'required', 'autocomplete': 'off', 'placeholder': 'Your Phone'}),
            'address': TextInput(attrs={'class': 'form-control', 'required': 'required', 'autocomplete': 'off', 'placeholder': 'Your address'}),
            'city': TextInput(attrs={'class': 'form-control', 'name': 'comments', 'rows': '5', 'data-msg-required': 'This field is required.', 'placeholder': 'Your city'}),
            'pin': TextInput(attrs={'class': 'form-control', 'name': 'comments', 'rows': '5', 'data-msg-required': 'This field is required.', 'placeholder': 'Your pin'}),
            'idproof': TextInput(attrs={'class': 'form-control', 'name': 'comments', 'rows': '5', 'data-msg-required': 'This field is required.', 'placeholder': 'Your idproof'}),

        }