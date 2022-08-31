from email.headerregistry import Address
from pyclbr import Class
from tabnanny import verbose
from django.db import models

# from phone_field import PhoneField

#Create your models here.

from home.models import User



class Kyc(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True)
    country = models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True,null=True)
    address = models.CharField(max_length=200 )
    city = models.CharField(max_length=100)
    pin = models.IntegerField()
    id_proof = models.CharField(max_length=100)
    id_proof_file = models.ImageField(upload_to='proof')
    live_photo = models.ImageField(upload_to='live photo')



    def __str__(self):
        return self.user.first_name
   


    


    
  