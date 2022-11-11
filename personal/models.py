import os

from django.db import models
from music import models as music_model

class user_info(models.Model):
    user_id = models.CharField('user_id', max_length=200,primary_key=True)
    user_name = models.CharField('user_name', max_length=200)
    user_email = models.EmailField('user_email')
    user_phone = models.CharField('user_email',max_length=200)

class user_fav(models.Model):#类名即为表名

    user_id = models.CharField('user_id',max_length=200)

    song_id = models.CharField('song_id',max_length=200)


class user_his(models.Model):

    user_id = models.CharField('user_id',max_length=200)

    song_id = models.CharField('song_id',max_length=200)

    p = models.IntegerField(default="")
    fractional_play_count = models.IntegerField(default=0)


