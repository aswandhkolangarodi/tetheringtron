from django.db import models

# Create your models here.
class Announcement(models.Model):
    Alert = models.CharField(max_length=200)