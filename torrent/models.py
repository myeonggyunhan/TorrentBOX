from django.db import models
from django.contrib.auth.models import User

class TorrentQuerySet(models.QuerySet):
    def copy_and_create(self, exist_torrent, new_owner):
        return self.create(
            name = exist_torrent.name,
            hash = exist_torrent.hash,
            size = exist_torrent.size,
            peers = exist_torrent.peers,
            status = exist_torrent.status,
            progress = exist_torrent.progress,
            download_rate = exist_torrent.download_rate,
            downloaded_size = exist_torrent.downloaded_size,
            owner = new_owner
        )
  
    def get_actives(self, owner):
        return self.filter(status='downloading') | self.filter(status='finished')


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

    objects = TorrentQuerySet.as_manager()

    class Meta:
        db_table = 'torrent_entries'
        verbose_name_plural = 'torrents'

    def __str__(self):
        return self.name

