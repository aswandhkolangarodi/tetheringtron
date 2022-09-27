from email.headerregistry import Address
from pyclbr import Class
from tabnanny import verbose
import uuid
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
    pin = models.IntegerField(null=True , blank=True)
    id_proof = models.CharField(max_length=100)
    id_proof_file = models.ImageField(upload_to='proof',null=True)
    member_image = models.ImageField(upload_to="member_image",null=True)
    live_photo = models.FileField(upload_to='live photo', null=True,blank=True)
    status= models.CharField(default="pending",max_length=50)
    reson = models.CharField(max_length=200, null=True, blank=True, default="")

    def __str__(self):
        return str(self.user)

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    test_id =models.UUIDField()
    amount = models.FloatField()
    txn_id = models.CharField(max_length=300)
    payment_status = models.CharField(max_length=100)
    trade_status = models.BooleanField(default=False)
    total_deposit = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.user)

class RewardEarnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    earnings = models.FloatField()
    
    def __str__(self):
        return str(self.user)

class ReffferalEarnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    earnings = models.FloatField() 

    def __str__(self):
        return str(self.user)

class Withdrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    amount = models.FloatField()
    trx_address = models.CharField(max_length=500)
    txn_id = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=100, default="pending")    
    

    def __str__(self):
        return str(self.user)


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    test_id =models.UUIDField(null=True)
    deposit = models.ForeignKey(Deposit , on_delete=models.CASCADE, blank=True,null=True)
    withdrow = models.ForeignKey(Withdrow , on_delete=models.CASCADE, blank=True,null=True)
    mode = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True) 
    deposit_status = models.CharField(max_length=100, null=True, default="unpaid")
    withdrowal_status = models.CharField(max_length=100, null=True, default="pending")

    def __str__(self):
        return str(self.user)
    
class WeeklyMemberEarnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class MemberTotalEarnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    earnings = models.FloatField()

    def __str__(self):
        return str(self.user)