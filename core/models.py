from django.db import models

class Entries(models.Model):
	name=models.CharField(max_length=100, null=True)
	hash_value=models.CharField(max_length=40, null=False)
	progress=models.FloatField(default=0, null=True)
