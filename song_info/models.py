from django.db import models

# Create your models here.
class song_his_temp(models.Model):
    song_id = models.CharField(max_length=250)
class song_rivew(models.Model):
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    review = models.CharField(max_length=5000)

