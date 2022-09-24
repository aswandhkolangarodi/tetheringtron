from pyexpat import model
from django.db import models
from home.models import User

# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    Alert = models.CharField(max_length=200)
    is_seen = models.BooleanField(default=False)

class AddReward(models.Model):
    refer_reward =models.CharField(max_length=100)
    youtube_reward = models.CharField(max_length=100)
    