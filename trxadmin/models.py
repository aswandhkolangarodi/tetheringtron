from django.db import models

# Create your models here.
class Announcement(models.Model):
    Alert = models.CharField(max_length=200)

class AddReward(models.Model):
    youtube_reward = models.CharField(max_length=100)