from email.headerregistry import Address
from pyclbr import Class
from tabnanny import verbose
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from phone_field import PhoneField

#Create your models here.


class Kyc(models.Model):
    
    full_name = models.CharField(max_length=100 )
    country = models.CharField(max_length=50)
    email = models.CharField(max_length=100 )
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
    address = models.CharField(max_length=200 )
    city = models.CharField(max_length=100)
    pin = models.IntegerField()
    id_proof = models.CharField(max_length=100)
    id_proof_file = models.FileField(upload_to='files')
    live_photo = models.FileField(upload_to='files')
    
   


    


    
  