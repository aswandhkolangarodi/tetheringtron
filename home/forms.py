from dataclasses import fields
from pyexpat import model
from tkinter import Widget
from django import forms
from .models import User
from django.forms.widgets import  SelectMultiple, TextInput, Textarea, EmailInput, CheckboxInput,URLInput, Select, NumberInput, RadioSelect, FileInput,ClearableFileInput, PasswordInput
# from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

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