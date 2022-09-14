
from django import forms
from django.forms.widgets import  SelectMultiple, TextInput, Textarea, EmailInput, CheckboxInput,URLInput, Select, NumberInput, RadioSelect, FileInput,ClearableFileInput, PasswordInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    phone = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial = "IN")
    )
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2','phone')
        widgets = {
            'username': TextInput(attrs={'class':'form-control', 'name':'username','placeholder':'username','required':'required','autocomplete':'off'}),
            'email' : TextInput(attrs={'class':'form-control', 'name':'email','placeholder':'email','required':'required','autocomplete':'off'}),
            'phone': TextInput(attrs={'class':'form-control', 'name':'phone','placeholder':'Phone Number','required':'required','autocomplete':'off'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}),
            'password2': TextInput(attrs={'class':'form-control', 'name':'password2','placeholder':'Confirm Password','required':'required','autocomplete':'off'})
        }
        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)

            for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None

# class UserPhone(forms.ModelForm):
    
#     class Meta:
#         model=User
#         fields = ('phone',)
#         widgets = {
#             'phone': TextInput(attrs={'class': ' form-control', })}


# class UsreRegistration(forms.ModelForm):

#     class Meta:
#         model=User
#         fields=('First_name','email','phone','password')