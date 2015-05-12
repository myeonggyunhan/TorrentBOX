from django.contrib import admin

# Register your models here.
from .models import Account, TorrentEntries

admin.site.register(Account)
admin.site.register(TorrentEntries) 
