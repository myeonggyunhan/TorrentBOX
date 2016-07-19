from django.db import models
from django.contrib.auth.models import User

class Torrent(models.Model):
    name = models.CharField(max_length=200)
    hash = models.CharField(max_length=40)
    size = models.BigIntegerField(default=0)
    peers = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20)
    progress = models.PositiveSmallIntegerField(default=0)
    download_rate = models.FloatField(default=0)
    downloaded_size = models.BigIntegerField(default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'torrent_entries'
        verbose_name_plural = 'torrents'

    def __str__(self):
        return self.name

