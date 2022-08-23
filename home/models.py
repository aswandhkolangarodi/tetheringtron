from email.policy import default
from turtle import update
from venv import create
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .utils import generate_ref_code
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    phone=models.CharField(max_length=15)
    user_img = models.ImageField(upload_to='user')

    
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    code = models.CharField(max_length=12,blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    updated = models.DateTimeField(auto_now=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    def get_recommended_profiles(self):
        pass

    def save(self,*args,**kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code 
        super().save(*args,**kwargs)