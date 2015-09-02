from django.db import models
from django.contrib.auth.models import User

# I created Custom User model for expandability
class Account(models.Model):
	user=models.OneToOneField(User)

class TorrentEntries(models.Model):
	name=models.CharField(max_length=100, null=True)
	hash_value=models.CharField(max_length=40, null=False)
	progress=models.PositiveSmallIntegerField(default=0, null=True)
	download_rate=models.FloatField(default=0, null=True)
	file_size=models.BigIntegerField(default=0, null=True)
	downloaded_size=models.BigIntegerField(default=0, null=True)
	peers=models.PositiveSmallIntegerField(default=0, null=True)
	status=models.CharField(max_length=20, null=True)
	worker_pid=models.PositiveIntegerField(default=0, null=True)

	# Download priority, 0 priority means that torrent is downloading status
	# if priority is not zero, then there exist more than one torrent in queue
	# It means worker is all active and user have to wait.
	priority=models.PositiveSmallIntegerField(default=0, null=True)

	# We can manage TorrentList for each user by using this ForeignKey
	owner=models.ForeignKey(Account)

# Server store all downloaded torrent entry information to prevent duplicated downloading
class TorrentGlobalEntries(models.Model):
	name=models.CharField(max_length=100, null=True)
	hash_value=models.CharField(max_length=40, null=False)
	progress=models.PositiveSmallIntegerField(default=0, null=True)
	file_size=models.BigIntegerField(default=0, null=True)
	downloaded_size=models.BigIntegerField(default=0, null=True)
	peers=models.PositiveSmallIntegerField(default=0, null=True)
	status=models.CharField(max_length=20, null=True)
