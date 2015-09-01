from django.shortcuts import HttpResponse, render, render_to_response, RequestContext, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account, TorrentEntries

import mimetypes
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Account, TorrentEntries, TorrentGlobalEntries

from django.conf import settings
from utils.func import *
from time import sleep
from api import tasks
import os
import signal
		
import libtorrent as lt
import requests

@login_required
def add_torrent(request):
	# TODO: Support magnet
	if request.FILES.has_key('torrent_file') is True:
		torrent_file = request.FILES['torrent_file']
		data = torrent_file.read()
	
	elif request.POST.has_key('torrent_url') is True:
		url = request.POST['torrent_url']
		val = URLValidator()
		try:
			val(url)
		except:
			messages.error(request, "Invalid torrent URL! Please check your torrent URL")
			return redirect("/")

		response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		data = response.content
	else:
		messages.error(request, "Please add torrent file by URL or file")
		return redirect("/")

	try:	
		e = lt.bdecode(data)
	except:
		messages.error(request, "Broken or invalid torrent file! Please check your torrent URL or file")
		return redirect("/")

	info = lt.torrent_info(e)
	torrent_hash = str(info.info_hash())

	# get current user information
	u = User.objects.get(username = request.user.username)
	account = Account.objects.get(user=u)

	# If current user have this torrent entry, then nothing todo. redirect to root.
	# TODO: notice this to user
	torrent_entry = TorrentEntries.objects.filter(owner=account, hash_value=torrent_hash)
	if torrent_entry:
		messages.error(request, "You already have this torrent")
		return redirect("/")

	#TODO: Try download same torrent more than two user at the same time
	# instead of duplicated downloading, we have to provide mirror of one
	# actually download only one torrent, others just get information of it not download it

	# Duplication check, if current user doesn't have this torrent entry but torrent file exist in server
	# then just update current user's torrent entry and redirect to root.
	# Since we don't have to re-download same file (file is already exist in server)
	torrent_entry = TorrentEntries.objects.filter(hash_value=torrent_hash).first()
	if torrent_entry and torrent_entry.progress == 100:
		new_entry=TorrentEntries(name=torrent_entry.name, hash_value=torrent_entry.hash_value,
					 progress=torrent_entry.progress, 
					download_rate=torrent_entry.download_rate, 
					owner=account,
                                       	file_size=torrent_entry.file_size, 
					downloaded_size=torrent_entry.downloaded_size, 
					peers=torrent_entry.peers,
                                       	status=torrent_entry.status)
		new_entry.save()
		return redirect("/")
	
	# Background torrent download	
	tasks.TorrentDownload.delay(account, data)
	return redirect("/")


@login_required
def torrent_status(request):
	u = User.objects.get(username=request.user.username)
	current_account = Account.objects.get(user=u)
	try:
		entries = TorrentEntries.objects.filter(owner=current_account)
	except:
		entries = None
	
	torrent_list = []
	torrent_info = {}

	for entry in entries:
		torrent_info['hash_value'] = entry.hash_value
		torrent_info['name'] = entry.name
		torrent_info['progress'] = entry.progress
		torrent_info['peers'] = entry.peers
		torrent_info['status'] = entry.status

		torrent_info['download_rate'] = unitConversion(entry.download_rate, "download_rate")
		torrent_info['file_size'] = unitConversion(entry.file_size, "file")
		torrent_info['downloaded_size'] = unitConversion(entry.downloaded_size, "file")

		if (entry.download_rate == 0) and (entry.status != "finished"):
			torrent_info['rtime'] = "unknown"
		elif (entry.download_rate == 0) and (entry.status == "finished"):
			torrent_info['rtime'] = "0 sec"
		else:
			rtime = (entry.file_size - entry.downloaded_size) / entry.download_rate
			torrent_info['rtime'] = unitConversion(rtime, "time")

		torrent_list.append(dict(torrent_info))

	return render_to_response("torrent_status.html", locals(), context_instance=RequestContext(request))

@login_required
def download(request):

	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		messages.error(request, "You have to select torrent to donwload")
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		messages.error(request, "You don't have this torrent! Please add it first")
		return redirect("/")

	# If download is not completed yet, redirect to root
	# TODO: we have to notice this to user
	if entry.progress != 100:
		messages.error(request, "You can't download file while torrent downloading.")
		return redirect("/")

	# To support large file transfer, use limited chunksize and StreamingHttpResponse	
	filename = os.path.join(settings.DOWNLOAD_DIR, str(entry.name))
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(filename), chunk_size), content_type=mimetypes.guess_type(filename)[0])
	response['Content-Length'] = os.path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=%s" % str(entry.name)
	return response

@login_required
def delete(request):
		
	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		messages.error(request, "You have to select torrent to remove.")
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		messages.error(request, "You don't have this torrent! Please add it first")
		return redirect("/")

	# If progress is 100%, then delete TorrentEntry from user DB
	# However, we don't delete real file from server
	if entry.progress == 100:
		entry.delete()

	# User cancel torrent download during download ...	
	else:
		os.kill(entry.worker_pid, signal.SIGINT)

	return redirect("/")
