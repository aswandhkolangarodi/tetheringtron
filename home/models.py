from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .utils import generate_ref_code
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone=models.CharField(max_length=100,null=True)
    user_img = models.ImageField(upload_to='user',null=True , blank=True)
    kyc_status=models.BooleanField(default=False)
    member_status= models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Profile(models.Model):

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    code = models.CharField(max_length=12,blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    recommended_by_status = models.BooleanField(default=False)
    first_deposit_status = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    auth_token = models.CharField(max_length=100 )
    forget_password_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def get_recommended_profiles(self):
        qs=Profile.objects.all()
        my_recs=[]
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        
        return my_recs

    def save(self,*args,**kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code 
        super().save(*args,**kwargs)

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    youtube = models.TextField(max_length=1000)
    status  = models.CharField(max_length=100, default="waiting for approval")
    reject_reson = models.CharField(max_length = 5000,blank=True,null=True)
    date = models.DateField(auto_now_add=True,null=True, blank=True)
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True, null=True)