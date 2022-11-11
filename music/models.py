from django.db import models

# Create your models here.
class Song_store(models.Model):
    #歌曲名
    title = models.CharField(max_length=200)
    #来源专辑
    source = models.CharField(max_length=200)
    #创作者
    writer = models.CharField(max_length=200)
    #创造年代
    age = models.IntegerField()
    #歌曲id
    song_id = models.CharField(primary_key=True,max_length=200)
    def __str__(self):
        return self.title