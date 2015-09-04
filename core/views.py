# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse
from account.models import Account, TorrentEntries
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from utils.func import *

@login_required
def home(request):
	template = "index.html"	
	
	username = request.user.username
	u = User.objects.get(username=request.user.username)
	current_account = Account.objects.get(user=u)

	try:
		entries = TorrentEntries.objects.filter(owner=current_account)
	except:
		entries = None

        torrent_list = list()
        torrent_info = dict()

        for entry in entries:
		if entry.status != "terminated":
			torrent_info['hash_value'] = entry.hash_value
			torrent_info['name'] = entry.name
			torrent_info['progress'] = entry.progress
			torrent_info['peers'] = entry.peers

			torrent_info['download_rate'] = unitConversion(entry.download_rate, "download_rate")
			torrent_info['file_size'] = unitConversion(entry.file_size, "file")
			torrent_info['downloaded_size'] = unitConversion(entry.downloaded_size, "file")
			torrent_info['status'] = entry.status
			torrent_info['priority'] = entry.priority

			if (entry.download_rate == 0) and (entry.status != "finished"):
				torrent_info['rtime'] = "unknown"
			elif (entry.download_rate == 0) and (entry.status == "finished"):
				torrent_info['rtime'] = "0 sec"
			else:
				rtime = (entry.file_size - entry.downloaded_size) / entry.download_rate
				torrent_info['rtime'] = unitConversion(rtime, "time")

			torrent_list.append(dict(torrent_info))

	return render_to_response(template,locals(),context_instance=RequestContext(request))
