from django.shortcuts import HttpResponse, render, render_to_response, RequestContext, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account, TorrentEntries

from celery.task.control import inspect
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

from api.tasks import TorrentDownload
import os
import signal
		
import libtorrent as lt
import requests
import time

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

		# TODO: SSL error occur, we have to fix it.
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
	torrent_entry = TorrentEntries.objects.filter(owner=account, hash_value=torrent_hash)
	if torrent_entry:
		messages.error(request, "You already have this torrent")
		return redirect("/")

	#TODO: Try download same torrent more than two user at the same time
	# instead of duplicated downloading, we have to provide mirror of one
	# actually download only one torrent, others just get information of it. Not download it

	# Duplication check, if current user doesn't have this torrent entry but torrent file exist in server
	# then just update current user's torrent entry and redirect to root. (this save worker thread)
	# Since we don't have to re-download same file (file is already exist in server)
	torrent_entry = TorrentGlobalEntries.objects.filter(hash_value=torrent_hash, status="finished").first()
	if torrent_entry:
		new_entry=TorrentEntries(name = torrent_entry.name,
					hash_value = torrent_entry.hash_value,
					progress = torrent_entry.progress, 
					download_rate = 0, 
					owner = account,
                                       	file_size = torrent_entry.file_size, 
					downloaded_size = torrent_entry.downloaded_size, 
					peers = torrent_entry.peers,
                                       	status = torrent_entry.status)
		new_entry.save()
		return redirect("/")

	# Calculate the number of waiting torrents in queue
	waitings=TorrentEntries.objects.filter(status="queued").count()
	waitings+=1	
	
	# Initialize new user torrent entry. status must be initialized with queued.
	new_entry=TorrentEntries(name = str(info.name()), 
				hash_value = str(torrent_hash),
				progress = 0,
				download_rate = 0,
				owner = account,
				file_size = int(info.total_size()),
				downloaded_size = 0,
				peers = 0, 
				status = "queued",
				priority = waitings)

	try:
		new_entry.save()
	except:
		messages.error(request, "Database insert error! Please notice this to admin")
		return redirect("/")

	# Background torrent download	
	TorrentDownload.delay(account, data)
	return redirect("/")


@login_required
def torrent_status(request):
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
			torrent_info['status'] = entry.status
			torrent_info['priority'] = entry.priority

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
	if entry.status != "finished":
		messages.error(request, "You can't download file until finished")
		return redirect("/")

	# To support large file transfer, use limited chunksize and StreamingHttpResponse	
	filename = os.path.join(settings.DOWNLOAD_DIR, str(entry.name))
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(filename), chunk_size), content_type=mimetypes.guess_type(filename)[0])
	response['Content-Length'] = os.path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=\"%s\"" % str(entry.name)
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

	if entry.status == "compressing":
		messages.error(request, "You can't remove torrent during compressing")
		return redirect("/")

	# Delete user's torrent entry. But, we don't delete real file from server.
	elif entry.status == "finished":
		entry.delete()

	# User cancel downloading torrent	
	elif entry.status == "downloading":
		os.kill(entry.worker_pid, signal.SIGINT)

	# We have to handle queued status
	elif entry.status == "queued":
		# Change status to terminated
		entry.status = "terminated"
		entry.save()

		# Update queued torrent's priority
		queued_entries = TorrentEntries.objects.filter(status="queued")
		for entry in queued_entries:
			if entry.priority != 0:
				entry.priority -= 1
				entry.save()

	return redirect("/")
