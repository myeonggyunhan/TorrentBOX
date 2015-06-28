from django.shortcuts import HttpResponse, render, render_to_response, RequestContext, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account, TorrentEntries

import mimetypes
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper

from django.contrib.auth.models import User
from account.models import Account, TorrentEntries

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

	# TODO: check uniqueness in view... not in task
	# to prevent high traffic to work queue
	if request.FILES.has_key('torrent_file') is True:
		print "DEBUG:: Torrent File upload..."
		torrent_file = request.FILES['torrent_file']
		data = torrent_file.read()
	
	elif request.POST.has_key('torrent_url') is True:
		print "DEBUG:: Torrent URL upload..."
		url = request.POST['torrent_url']
		response = requests.get(url)
		data = response.content
	else:
		#TODO: notificate to user, error!
		print "DEBUG:: Not supported yet..."
		return redirect("/")

	e = lt.bdecode(data)
	info = lt.torrent_info(e)
	torrent_hash = str(info.info_hash())

	# get current user information
	u = User.objects.get(username = request.user.username)
	account = Account.objects.get(user=u)

	# check uniqueness
	torrent_entry = TorrentEntries.objects.filter(hash_value=torrent_hash).first()
	if torrent_entry and torrent_entry.progress == 100.0:
		new_entry=TorrentEntries(name=torrent_entry.name, hash_value=torrent_hash,
					 progress=torrent_entry.progress, 
					download_rate=torrent_entry.download_rate, 
					owner=account,
                                       	file_size=torrent_entry.file_size, 
					downloaded_size=torrent_entry.downloaded_size, 
					peers=torrent_entry.peers,
                                       	status=torrent_entry.status, 
					worker_pid=os.getpid())
		new_entry.save()
		return redirect("/")
	
	# Background torrent download	
	tasks.TorrentDownload.delay(account, data)
	return redirect("/")


@login_required
def list_progress(request):
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

                torrent_info['download_rate'] = unitConversion(entry.download_rate, "download_rate")
                torrent_info['file_size'] = unitConversion(entry.file_size, "file")
                torrent_info['downloaded_size'] = unitConversion(entry.downloaded_size, "file")

	
		if entry.status == "finished":
			torrent_info['rtime'] = "Finished!"
       
		elif entry.status == "compressing":
			torrent_info['rtime'] = "Compressing data..."
	        	
		elif entry.download_rate == 0:
                        torrent_info['rtime'] = "remaining time unknown"
        
	        else:
                        rtime = (entry.file_size - entry.downloaded_size) / entry.download_rate
                        torrent_info['rtime'] = unitConversion(rtime, "time") + " remaining"

                torrent_list.append(dict(torrent_info))

        return render_to_response("list_progress.html", locals(), context_instance=RequestContext(request))

@login_required
def download(request):

	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		return redirect("/")

	# If download is not completed yet, redirect to root
	# TODO: we have to notice this to user
	# TODO: How about streaming download?
	if entry.progress != 100.0:
		return redirect("/")

	# To support large file transfer, use limited chunksize and StreamingHttpResponse	
	filename = settings.DOWNLOAD_DIR + str(entry.name)
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(filename), chunk_size), content_type=mimetypes.guess_type(filename)[0])
	response['Content-Length'] = os.path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=%s" % str(entry.name)
	return response

@login_required
def delete(request):
		
	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		return redirect("/")

	# If progress is 100%, then delete TorrentEntry from user DB
	# However, we don't delete real file from server
	if entry.progress == 100.0:
		entry.delete()

	# User cancel torrent download during download ...	
	else:
		os.kill(entry.worker_pid, signal.SIGINT)

	return redirect("/")

	
'''
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entries = TorrentEntries.objects.filter(owner=current_account)
        except:
                entries = None

	torrent_list = []
	torrent_info = {}
	
	for entry in entries:
		print entry.hash_value
		torrent_info['hash_value'] = entry.hash_value
		torrent_info['name'] = entry.name

		# Custom DATA
		torrent_info['rtime'] = 300
		torrent_list.append(dict(torrent_info))
'''
def debug(request):

	torrent_hash = request.GET.get('torrent_hash','')
	torrent_entry = TorrentEntries.objects.filter(hash_value=torrent_hash).first()

	entries = TorrentEntries.objects.filter(hash_value=torrent_hash)
	for entry in entries:
		print entry.owner.user.username

	print ":: TEST DEBUG START ::"
	if torrent_entry:
		print torrent_entry.owner.user.username
		if torrent_entry.progress == 100.0:
			print "100 percent!"
	else:
		print "No such torrent exist in DB"

        return render_to_response("debug.html", locals(), context_instance=RequestContext(request))
	
'''
	if TorrentEntries.objects.filter(hash_value=torrent_hash).exists() is True:
		entries = TorrentEntries.objects.filter(hash_value=torrent_hash)

		# get first single entry
		for entry in entries:
			torrent_entry = entry
			break
		
		print torrent_entry.owner.user.username	
	
'''





