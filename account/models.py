from django.db import models
from django.contrib.auth.models import User

# I created Custom User model for expandability
class Account(models.Model):
	user=models.OneToOneField(User)

class TorrentEntries(models.Model):
        name=models.CharField(max_length=100, null=True)
        hash_value=models.CharField(max_length=40, null=False)
        progress=models.FloatField(default=0, null=True)
	download_rate=models.FloatField(default=0, null=True)

	# We can manage TorrentList for each user by using this ForeignKey
	owner=models.ForeignKey(Account)
